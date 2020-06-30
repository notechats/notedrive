from notedrive.lanzou import LanZouCloud

downer = LanZouCloud()
downer.ignore_limits()
downer.login_by_cookie()


def test1():
    print(downer.login_by_cookie() == LanZouCloud.SUCCESS)


def test2():
    def callback(file_name, total_size, now_size):
        print("\r文件名:{file_name}, 进度: {now_size}/{total_size}".format(file_name=file_name,
                                                                      now_size=now_size,
                                                                      total_size=total_size))
        file_path = '/Users/liangtaoniu/workspace/MyDiary/tmp/weights/yolov3.weight'
        downer.upload_file(file_path=file_path, callback=callback)


def test3():
    downer.down_dir_by_url('https://wws.lanzous.com/b01hh292j')


def test4():
    downer.upload_file('/Users/liangtaoniu/workspace/dataset/tianchi001/trainset.zip', folder_id=2010460)
    downer.upload_file('/Users/liangtaoniu/workspace/dataset/tianchi001/test_input.zip', folder_id=2010460)


def test5():
    print(downer.get_dir_list(folder_id=2010460))


test5()
