import concurrent.futures
import os
from threading import Lock
from time import sleep

import numpy as np
import pycurl
from requests import Session
from tqdm import tqdm

from notetool.tool import exists_file, delete_file, path_parse
from notetool.tool import log


class BaseDownLoad:
    def __init__(self, session=None):
        self.url = None
        self.path = None
        self.size = None
        self.session = session or Session()
        self.logger = log(__name__)
        self.logger.debug(self.session.headers)

    def download(self, url, path, size=0, overwrite=False):
        path = path_parse(path)
        self.url = url
        self.path = path
        if exists_file(file_path=path, mkdir=True):
            if overwrite:
                delete_file(file_path=path)
            else:
                self.logger.info('file exist and return[path={}].'.format(path))
                return
        else:
            self.init_path(path)

        file_name = os.path.basename(path)
        self.logger.info("download {} from {} to {} ".format(file_name, url, path))
        self._download(url, path, size=size)
        self.logger.info('download {} success'.format(file_name))

    def _download(self, url, path, size=0):
        pass

    @staticmethod
    def init_path(path):
        local_dir = os.path.dirname(path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)


class MultiThreadDownload(BaseDownLoad):
    def __init__(self, worker=5, chunk_size=10 * 1024 * 1024, *args, **kwargs):
        self.lock = Lock()
        self.num = worker
        self.worker = worker
        self.chunk_size = chunk_size
        self.down_btn = None
        super(MultiThreadDownload, self).__init__(*args, **kwargs)

    def down(self, start, end):
        headers = {'Range': 'bytes={}-{}'.format(start, end)}
        # stream = True 下载的数据不会保存在内存中
        r = self.session.get(self.url, headers=headers)
        # 写入文件对应位置,加入文件锁
        self.lock.acquire()
        print(r.status_code)

        with open(self.path, "rb+") as fp:
            fp.seek(start)
            fp.write(r.content)
            self.lock.release()
            # 释放锁
        self.down_btn.update(1)

    def _download(self, url, path, size=0, **kwargs):
        if size == 0:
            r = self.session.head(self.url)

            # 若资源显示302,则迭代找寻源文件
            # while r.status_code == 302:
            #     self.url = r.headers['Location']
            #     logger.warning("该url已重定向至{}".format(self.url))
            #     r = self.session.head(self.url)

            self.size = int(r.headers['Content-Length'])
        else:
            self.size = size

        self.logger.info('该文件大小为：{} bytes'.format(self.size))
        self.num = self.size // self.chunk_size + 1

        self.down_btn = tqdm(total=self.num)
        # 创建一个和要下载文件一样大小的文件
        with open(self.path, "wb") as fp:
            fp.truncate(self.size)

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.worker)

        # 启动多线程写文件
        futures = []

        for i in range(self.num):
            start = self.chunk_size * i
            # 最后一块
            if i == self.num - 1:
                end = self.size
            else:
                end = start + self.chunk_size + 1
            sleep(0.5)
            futures.append(pool.submit(self.down, start, end))
        concurrent.futures.wait(futures)


class SingleThreadDownload(BaseDownLoad):
    """
    HTTP下载较大文件的工具
    """

    def __init__(self, chunk=1024 * 1024, *args, **kwargs):
        self.position = 0  # 当前的字节偏移量
        self.chunk = chunk

        super(SingleThreadDownload, self).__init__(*args, **kwargs)

    def _download(self, url, path, size=0):
        file_size = size
        local_path = path
        file_name = os.path.basename(local_path)

        if os.path.exists(local_path):
            first_byte = os.path.getsize(local_path)
        else:
            first_byte = 0

        self.init_path(local_path)

        position = first_byte

        mode = 'ab' if first_byte > 0 else 'wb'
        with open(local_path, mode=mode) as f:
            with tqdm(initial=np.round(first_byte / self.chunk, 2),
                      total=np.round(file_size / self.chunk, 2),
                      unit='MB',
                      desc=file_name) as pbar:
                while position < file_size:
                    interval = (position, position + self.chunk)
                    position += (self.chunk + 1)

                    time = 3
                    while time > 0:
                        try:
                            resp = self.session.get(url, headers={'Range': 'bytes=%s-%s' % interval})
                            f.write(resp.content)
                            pbar.update(1)
                            break
                        except Exception as e:
                            time -= 1
                            self.logger.warning(e)

        return True


class PyCurlDownLoad(BaseDownLoad):
    def __init__(self, *args, **kwargs):
        super(PyCurlDownLoad, self).__init__(*args, **kwargs)

    def _download(self, url, path, size=0):
        with open(self.path, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(pycurl.URL, self.url)
            c.setopt(pycurl.WRITEDATA, f)
            c.perform()
            c.close()


def download(url, path, size=0, session=None, overwrite=False, mode='curl'):
    if mode == 'curl':
        down = PyCurlDownLoad()
    elif mode == 'single':
        down = SingleThreadDownload(session=session)
    else:
        down = MultiThreadDownload(session=session)
    down.download(url, path, size, overwrite=overwrite)
