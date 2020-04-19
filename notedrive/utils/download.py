import os

import pycurl

from notedrive.baidu.drive import BaiDuDrive


def download(url, path):
    with open(path, 'wb') as f:
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEDATA, f)
        c.perform()
        c.close()


def download_from_url(url, bduss=None, save_path='/drive/temp/'):
    client = BaiDuDrive(bduss)
    filename = os.path.basename(url)
    download(url, filename)
    client.upload(filename, save_path + filename, overwrite=True)
