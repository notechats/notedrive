# 概述
1.支持百度云盘、蓝奏云盘的上传、下载  
2.百度云盘分享链接经常失效、蓝奏云永久有效


# 使用场景
数据产出后直接上传备份  
1.网上爬取的数据  
2.模型训练的结果  
3.大一点的数据集  


# 分类
|序号|网盘|文档|实例|支持内容|
|:--:|:--|:--|:--|:--|
|1|基础下载|[doc](https://github.com/notechats/notedrive/tree/master/notedrive/base/README.md)|[example](https://github.com/notechats/notedrive/blob/master/example/base_example.py)|多线程下载|
|2|百度云|[doc](https://github.com/notechats/notedrive/tree/master/notedrive/baidu/README.md)|[example](https://github.com/notechats/notedrive/blob/master/example/baidu_example.py)|上传、下载|
|3|蓝奏云|[doc](https://github.com/notechats/notedrive/tree/master/notedrive/lanzou/README.md)|[example](https://github.com/notechats/notedrive/blob/master/example/lanzou_example.py)|上传、下载|



# 安装

```bash
pip install notedrive
```
或者直接从GitHub安装
```bash
pip install git+https://github.com/notechats/notedrive.git
```


# 为啥要做这个
1.工作学习中经常用的数据集，尤其是国外数据集，下载速度贼慢  
2.网上找数据比较麻烦  
3.预借助蓝奏云，将一些国内外公开数据集放到一起，整理到[notedata](https://github.com/notechats/notedata)


#参考
百度云盘的python-api，[官方API](https://openapi.baidu.com/wiki/index.php?title=docs/pcs/rest/file_data_apis_list)  
蓝奏云的python-api [参考](https://github.com/zaxtyson/LanZouCloud-API)

