import os
from queue import Queue
from threading import Thread, Lock, current_thread
from urllib import parse

from requests import Session

APP_ID = 266719  # The app_id of ES file explore on android.
BASE_URL = 'http://pcs.baidu.com/rest/2.0/pcs'


class SuperDownloader(object):
    """HTTP下载较大文件的工具
    """

    def __init__(self,
                 url,
                 session,
                 save_path,
                 thread_num=45,
                 queue_size=10,
                 chunk=102400):
        """
        :param url: 资源链接
        :param session: 构造好上下文的session
        :param save_path: 保存路径
        :param thread_num: 下载线程数
        :param queue_size: 队列的大小，默认10
        :param chunk: 每个线程下载的块大小
        """
        self.url = url
        self.session = session
        self.save_path = save_path
        self.thread_num = thread_num
        self.queue = Queue(queue_size)
        self.file_size = self._content_length()
        self.position = 0  # 当前的字节偏移量
        self.chunk = chunk
        self.mutex = Lock()  # 资源互斥锁
        self.flags = [False] * self.thread_num

    def download(self):
        with open(self.save_path, 'wb') as fp:
            theads = []
            for i in range(self.thread_num):
                p = Thread(target=self._produce, name='%d' % i)
                theads.append(p)
                p.start()
            c = Thread(target=self._consume, args=(fp,), name='consumer')
            theads.append(c)
            c.start()
            for t in theads:
                t.join()

    def _produce(self):
        while True:
            if self.mutex.acquire():
                if self.position > self.file_size - 1:
                    self.flags[int(current_thread().getName())] = True
                    self.mutex.release()
                    return
                interval = (self.position, self.position + self.chunk)
                self.position += (self.chunk + 1)
                self.mutex.release()
            resp = self.session.get(
                self.url, headers={'Range': 'bytes=%s-%s' % interval})
            if not self.queue.full():
                self.queue.put((interval, resp.content))

    def _consume(self, fp):
        while True:
            if all(self.flags) and self.queue.empty():
                return
            if not self.queue.empty():
                item = self.queue.get()
                fp.seek(item[0][0])
                fp.write(item[1])

    def _content_length(self):
        """发送head请求获取content-length
        """
        resp = self.session.head(self.url)
        length = resp.headers.get('content-length')
        if length:
            return int(length)
        else:
            raise Exception('%s don\'t support Range' % self.url)


class BaiDuDrive(object):
    """A client for the PCS API.
    """

    def __init__(self, bduss, session=None, timeout=None):
        """
        :param bduss: The value of baidu cookie key `BDUSS`.
        """
        self.bduss = bduss
        self.session = session or Session()
        self.timeout = timeout
        # Add core auth cookie
        self.session.headers.update({'Cookie': 'BDUSS=%s' % self.bduss})

    def quota(self):
        """获得配额信息
        :return requests.Response

            .. note::
                返回正确时返回的 Reponse 对象 content 中的数据结构

                {"errno":0,"total":配额字节数,"used":已使用字节数,"request_id":请求识别号}
        """

        return self.get('/quota', dict(method='info'))

    def download(self, yun_path, local_path=None):
        """下载文件
        当local_path为None时，文件会保存在工作目录下，文件名默认为网盘的文件名。
        当local_path以/结尾时，文件名默认为网盘的文件名
        :param yun_path: 网盘下的文件路径
        :param local_path: 保存本地的文件路径
        """
        yun_dir, yun_filename = os.path.split(yun_path)
        cwd = os.getcwd()
        if local_path is None:
            local_dir = cwd
            local_filename = yun_filename
        else:
            local_dir, local_filename = os.path.split(local_path)
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            if not local_filename:
                local_filename = yun_filename
        local_path = os.path.join(local_dir, local_filename)

        params = {'method': 'download', 'app_id': APP_ID, 'path': yun_path}
        query_string = parse.urlencode(params)

        url = BASE_URL + '/file?%s' % query_string
        super_downloader = SuperDownloader(url, self.session, local_path)
        super_downloader.download()
        return True

    def upload(self, local_path, yun_path, ondup=True):
        """上传文件
        :param local_path: 本地文件路径
        :param yun_path: 云端文件路径
        :param ondup: 是否覆盖同名文件，默认覆盖
        """
        if ondup:
            ondup = 'overwrite'
        else:
            ondup = 'newcopy'
        params = {'method': 'upload', 'path': yun_path, 'ondup': ondup}
        files = {yun_path: open(local_path, 'rb')}
        return self.request('POST', '/file', params=params, files=files)

    def mkdir(self, yun_path):
        """创建目录
        :param yun_path: 云端文件夹路径
        """
        params = {'method': 'mkdir', 'path': yun_path}
        return self.request('POST', '/file', params=params)

    def delete(self, yun_path):
        """删除文件或者目录
        :param yun_path: 云端文件路径
        """
        if yun_path:
            # pass
            return

        params = {'method': 'delete', 'path': yun_path}
        return self.request('POST', '/file', params=params)

    def list(self, yun_path, by='name'):
        pass

    def get(self, uri, params):
        return self.request('GET', uri, params=params)

    def request(self, method, uri, headers=None, params=None, data=None, files=None, stream=None):
        if params is None:
            params = {}
        params.update({'app_id': APP_ID})
        url = BASE_URL + uri
        resp = self.session.request(method, url,
                                    headers=headers,
                                    params=params,
                                    data=data,
                                    files=files,
                                    timeout=self.timeout,
                                    stream=stream)

        return resp.json()
