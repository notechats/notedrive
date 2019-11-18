# coding: UTF-8
import requests
from bs4 import BeautifulSoup

url = "https://openapi.baidu.com/wiki/index.php?title=docs/pcs/rest/file_data_apis_list"

r = requests.get(url)
r.encoding = r.apparent_encoding
# 将源代码保存到变量s里面
s = r.text
soup = BeautifulSoup(s, "html.parser")
s = soup.prettify()
print(s)
