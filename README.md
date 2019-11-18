
# 说明
百度云盘的python-api，[官方API](https://openapi.baidu.com/wiki/index.php?title=docs/pcs/rest/file_data_apis_list)


# 安装

```bash
pip install notedrive
```
```bash
pip install git+https://github.com/notechats/notedrive.git
```

# 使用
## 第一次使用
获取百度cookies中的BDUSS值，注意保密
```python
from notedrive.baidu.drive import BaiDuDrive
client = BaiDuDrive(bduss="",save=True)
```
第一次使用后，会将BDUSS存入'~/.secret/.bduss'(save=True时)

如果允许保存到本地，则下次调用不用传入dbuss,即
```python
from notedrive.baidu.drive import BaiDuDrive
client = BaiDuDrive()
```

## list 查看
```python
from notedrive.baidu.drive import BaiDuDrive

client = BaiDuDrive()
for path in client.list("/drive/example/api"):
    print(path['server_filename'])
```

## meta 查看
```python
from notedrive.baidu.drive import BaiDuDrive

client = BaiDuDrive()
print(client.meta("/drive/example/api/test.txt"))
```

## upload 上传
```python
from notedrive.baidu.drive import BaiDuDrive

client = BaiDuDrive()
client.upload('test.txt', '/drive/example/api/test.txt', overwrite=False)
```

## download 上传
```python
from notedrive.baidu.drive import BaiDuDrive

client = BaiDuDrive()
client.download( '/drive/example/api/test.txt','test2.txt', overwrite=False)
```

## upload_dir 上传 TODO

## download_dir 上传 TODO




#参考

[baidupcsapi](https://github.com/ly0/baidupcsapi)

[baidu-pcs-python-sdk](https://github.com/mozillazg/baidu-pcs-python-sdk)


