import random

from expiringdict import ExpiringDict


class ForgetfulPeerStorage:
    def __init__(self, ttl=3600):
        self._ttl = ttl
        self._data = ExpiringDict(max_age_seconds=ttl, max_len=2000)
        self.data = ExpiringDict(max_age_seconds=ttl, max_len=2000)

    def get_peers(self, info_hash):
        if info_hash not in self._data:
            return []
        return self._data[info_hash].keys()

    def insert_peer(self, info_hash, peer):
        self.data[info_hash][peer] = None
        self.data[info_hash] = self.data[info_hash]


class ForgetfulTokenStorage:
    def __init__(self, ttl=600):
        self._data = ExpiringDict(max_age_seconds=ttl, max_len=2000)

    def get_token(self, sender, id, info_hash):
        token = bytes([random.randint(0, 255) for _ in range(16)])
        self._data[token] = (sender[0], id, info_hash)
        return token

    def verify_token(self, sender, id, info_hash, token):
        if self._data.get(token) == (sender[0], id, info_hash):
            del self._data[token]
            return True
        return False
