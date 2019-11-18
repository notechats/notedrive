from notedrive.baidu.drive import BaiDuDrive

client = BaiDuDrive()

for path in client.list("/drive/example/api"):
    print(path['server_filename'])

# client.upload('test.txt', '/drive/example/api/test.txt', overwrite=False)
# client.download('/temp.txt', 'temp.txt')

client.download('/drive/example/api/test.txt', 'test2.txt', overwrite=False)
