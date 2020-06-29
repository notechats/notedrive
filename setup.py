import sys
from os import path

from setuptools import setup, find_packages

from notetool.tool import get_version

version_path = path.join(path.abspath(path.dirname(__file__)), 'script/__version__.md')

version = get_version(sys.argv, version_path, step=16)

install_requires = ['requests', 'demjson', 'numpy', 'tqdm', 'cryptography', 'pycurl', 'notetool', 'urllib3']

setup(name='notedrive',
      version=version,
      description='notedrive',
      author='niuliangtao',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',

      packages=find_packages(),
      install_requires=install_requires
      )
