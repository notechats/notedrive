from notedrive.baidu.drive import BaiDuDrive

client = BaiDuDrive()

for path in client.list_deep("/drive/example/api"):
    print(path['path'])

# client.upload('test.txt', '/drive/example/api/test.txt', overwrite=False)
# client.download('/temp.txt', 'temp.txt')

client.download('/drive/example/api/test.txt', 'test3.txt', overwrite=False)

# client.upload_dir('/Users/liangtaoniu/workspace/MyDiary/logs', '/drive/example/api/')

#
# source_file = '/Users/liangtaoniu/workspace/MyDiary/tmp/dataset/data-science-bowl-2019/train.csv'
# target_dir = '/Users/liangtaoniu/workspace/MyDiary/tmp/dataset/data-science-bowl-2019/'
#
# split_file(source_file, target_dir, max_line=500000)
#
# print(client.offline_task_list())
# print(client.offline_task_add(
#     source_url='ed2k://|file|%E8%A1%8C%E5%B0%B8%E8%B5%B0%E8%82%89.The.Walking.Dead.S02E01.%E4%B8%AD%E8%8B%B1%E5%AD%97%E5%B9%95.BDrip.1080P-%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86.mp4|910568992|ABFB39A113E173197D4AD2D21E5D2CB8|h=7BLB2TLX3KKQXLGO553D6BFKWKG5PYW7|/'))
