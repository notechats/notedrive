#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/30 12:10
# @Author  : niuliangtao
# @Site    :
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup, find_packages

install_requires = ['requests', 'demjson', 'numpy', 'tqdm', 'cryptography', 'pycurl', 'notetool']

setup(name='notedrive',
      version='0.3.0',
      description='notedrive',
      author='niuliangtao',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',

      packages=find_packages(),
      install_requires=install_requires
      )
