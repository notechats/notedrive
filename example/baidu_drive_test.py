from notedrive.baidu.drive import BaiDuDrive, split_file

client = BaiDuDrive()

for path in client.list_deep("/drive/example/api"):
    print(path['path'])

# client.upload('test.txt', '/drive/example/api/test.txt', overwrite=False)
# client.download('/temp.txt', 'temp.txt')

client.download('/drive/example/api/test.txt', 'test2.txt', overwrite=False)

# client.upload_dir('/Users/liangtaoniu/workspace/MyDiary/logs', '/drive/example/api/')


source_file = '/Users/liangtaoniu/workspace/MyDiary/tmp/dataset/data-science-bowl-2019/train.csv'
target_dir = '/Users/liangtaoniu/workspace/MyDiary/tmp/dataset/data-science-bowl-2019/'

split_file(source_file, target_dir, max_line=500000)
