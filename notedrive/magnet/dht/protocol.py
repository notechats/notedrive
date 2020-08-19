import asyncio
import hashlib
import os
import random
import struct
from base64 import b64encode
from ipaddress import IPv4Address

from notetool.tool.log import log
from .node import Node
from .routing import RoutingTable
from ..bencode import BTFailure, bdecode, bencode

"""
Some code taken from
https://github.com/bmuller/rpcudp/blob/master/rpcudp/protocol.py
Has same license as kademlia, see __init__.py
"""

logger = log(__name__)
MIN_ID = 0
MAX_ID = 2 ** 160


class KRPCProtocol(asyncio.DatagramProtocol):
    def __init__(self, source_node, peer_storage, token_storage, ksize, wait_timeout=5, buckets=None, ):
        self.router = RoutingTable(self, ksize, source_node, buckets=buckets)
        self.peer_storage = peer_storage
        self.token_storage = token_storage
        self.source_node = source_node
        self._wait_timeout = wait_timeout
        self._outstanding = {}
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        logger.debug("received datagram from %s", addr)
        try:
            data = bdecode(data)
        except (BTFailure, ValueError, KeyError):
            logger.info("Failed to decode message")
            return

        if not isinstance(data, dict):
            return

        query_type = data.get(b"y")
        transaction_id = data.get(b"t")
        if not transaction_id:
            return

        if query_type == b"q":  # query
            args = data.get(b"a")
            func_name = data.get(b"q")
            if func_name and isinstance(args, dict):
                asyncio.ensure_future(
                    self.handle_request(transaction_id, func_name, args, addr)
                )
        elif query_type == b"r":  # response
            args = data.get(b"r")
            if isinstance(args, dict):
                asyncio.ensure_future(self.handle_response(transaction_id, args, addr))
        else:
            return

    async def handle_request(self, transaction_id, func_name, args, addr):
        func = getattr(self, "rpc_{}".format(func_name.decode('utf-8')), None)
        if func is None or not callable(func):
            msgargs = (self.__class__.__name__, func_name)
            logger.info("%s has no callable method " "rpc_%s; ignoring request", *msgargs)
            return

        if not asyncio.iscoroutinefunction(func):
            func = asyncio.coroutine(func)
        args = {k.decode("utf-8"): v for (k, v) in args.items()}
        response = await func(addr, **args)
        if response is not None:
            logger.debug(
                "sending response %s for msg id %s to %s",
                response,
                b64encode(transaction_id),
                addr,
            )
            txdata = bencode({b"y": b"r", b"r": response, })
            self.transport.sendto(txdata, addr)

    async def handle_response(self, transaction_id, args, addr):
        msgargs = (b64encode(transaction_id), addr)
        if transaction_id not in self._outstanding:
            logger.info("received unknown message %s " "from %s; ignoring", *msgargs)
            return
        logger.debug("received response %s for message " "id %s from %s", args, *msgargs)
        future, timeout = self._outstanding[transaction_id]
        timeout.cancel()
        if not future.cancelled():
            future.set_result((True, args))
        del self._outstanding[transaction_id]

    def _timeout(self, transaction_id):
        args = (b64encode(transaction_id), self._wait_timeout)
        logger.info("Did not received reply for msg " "id %s within %i seconds", *args)
        future = self._outstanding[transaction_id][0]
        if not future.cancelled():
            future.set_result((False, None))
        del self._outstanding[transaction_id]

    def get_refresh_ids(self):
        """
        Get ids to search for to keep old buckets up to date.
        """
        ids = []
        for bucket in self.router.lonely_buckets():
            rid = random.randint(*bucket.range).to_bytes(20, byteorder="big")
            ids.append(rid)
        return ids

    def is_valid_node_id(self, node):
        return MIN_ID < node.long_id < MAX_ID

    def rpc_ping(self, sender, id):
        source = Node(id, sender[0], sender[1])
        if not self.is_valid_node_id(source):
            return
        self.welcome_if_new(source)
        return {b"id": id}

    def rpc_announce_peer(
            self,
            sender,
            id,
            info_hash,
            port,
            token,
            name=None,
            implied_port=None,
            seed=None,
    ):
        source = Node(id, sender[0], sender[1])
        if not self.is_valid_node_id(source):
            return

        self.welcome_if_new(source)
        if self.token_storage.verify_token(sender[0], id, info_hash, token):
            if implied_port:
                port = sender[1]
            logger.debug("got an announce_peer request from %s, storing '%s'", sender, info_hash.hex(), )
            self.peer_storage.insert_peer((sender[0], port))
        else:
            logger.debug("Invalid token from %s", sender)
        return {b"id": id}

    def rpc_find_node(self, sender, id, target, want="n4", token=None):
        logger.info("finding neighbors of %i in local table", int(id.hex(), 16))
        source = Node(id, sender[0], sender[1])
        if not self.is_valid_node_id(source):
            return

        self.welcome_if_new(source)
        node = Node(target)
        if not self.is_valid_node_id(node):
            return
        neighbors = self.router.find_neighbors(node, exclude=source)
        data = {b"id": id, b"nodes": b"".join([n.packed for n in neighbors])}
        if token:
            data[b"token"] = token
        return data

    def rpc_get_peers(
            self, sender, id, info_hash, want="n4", noseed=0, scrape=0, bs=None
    ):
        source = Node(id, sender[0], sender[1])
        if not self.is_valid_node_id(source):
            return
        self.welcome_if_new(source)
        peers = self.peer_storage.get_peers(info_hash)
        token = self.token_storage.get_token(sender, id, info_hash)
        if not peers:
            return self.rpc_find_node(sender, id, info_hash, token=token)

        return {
            b"id": id,
            b"token": token,
            b"values": [
                IPv4Address(peer[0]).packed + struct.pack("!H", peer[1])
                for peer in peers
            ],
        }

    async def call_find_node(self, node_to_ask, node_to_find):
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.find_node(address, {b"id": self.source_node.id, b"target": node_to_find.id})
        return self.handle_call_response(result, node_to_ask)

    async def call_get_peers(self, node_to_ask, node_to_find):
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.get_peers(address, {b"id": self.source_node.id, b"info_hash": node_to_find.id})
        return self.handle_call_response(result, node_to_ask)

    async def call_ping(self, node_to_ask):
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.ping(address, {b"id": self.source_node.id})
        return self.handle_call_response(result, node_to_ask)

    async def call_announce_peer(self, node_to_ask, key, value):  # TODO
        address = (node_to_ask.ip, node_to_ask.port)
        result = await self.store(address, self.source_node.id, key, value)
        return self.handle_call_response(result, node_to_ask)

    def welcome_if_new(self, node):
        """
        Given a new node, send it all the keys/values it should be storing,
        then add it to the routing table.

        @param node: A new node that just joined (or that we just found out
        about).

        Process:
        For each key in storage, get k closest nodes.  If newnode is closer
        than the furtherst in that list, and the node for this server
        is closer than the closest in that list, then store the key/value
        on the new node (per section 2.5 of the paper)
        """
        if not self.router.is_new_node(node):
            return

        logger.info("never seen %s before, adding to router", node)
        self.router.add_contact(node)

    def handle_call_response(self, result, node):
        """
        If we get a response, add the node to the routing table.  If
        we get no response, make sure it's removed from the routing table.
        """
        if not result[0]:
            logger.info("no response from %s, removing from router", node)
            self.router.remove_contact(node)
            return result

        logger.info("got successful response from %s", node)
        self.welcome_if_new(node)
        return result

    def generate_token(self):
        return bytes([random.randint(0, 255) for _ in range(16)])

    def __getattr__(self, name):
        """
        If name begins with "_" or "rpc_", returns the value of
        the attribute in question as normal.
        Otherwise, returns the value as normal *if* the attribute
        exists, but does *not* raise AttributeError if it doesn't.
        Instead, returns a closure, func, which takes an argument
        "address" and additional arbitrary args (but not kwargs).
        func attempts to call a remote method "rpc_{name}",
        passing those args, on a node reachable at address.
        """
        if name.startswith("_") or name.startswith("rpc_"):
            return getattr(super(), name)

        try:
            return getattr(super(), name)
        except AttributeError:
            pass

        def func(address, args):
            transaction_id = hashlib.sha1(os.urandom(32)).digest()
            txdata = bencode({b"y": b"q", b"t": transaction_id, b"a": args, b"q": name.encode("utf-8"), })
            logger.debug("calling remote function %s on %s (msgid %s)", name, address, b64encode(transaction_id), )
            self.transport.sendto(txdata, address)

            loop = asyncio.get_event_loop()
            if hasattr(loop, "create_future"):
                future = loop.create_future()
            else:
                future = asyncio.Future()
            timeout = loop.call_later(self._wait_timeout, self._timeout, transaction_id)
            self._outstanding[transaction_id] = (future, timeout)
            return future

        return func
