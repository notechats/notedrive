from notedrive.lanzou import LanZouCloud, CodeDetail

downer = LanZouCloud()
downer.ignore_limits()
downer.login_by_cookie()


def example1():
    print(downer.login_by_cookie() == CodeDetail.SUCCESS)


def example2():
    file_path = '/Users/liangtaoniu/workspace/MyDiary/tmp/weights/yolov3.weight'
    downer.upload_file(file_path=file_path)


def example3():
    # downer.down_dir_by_url('https://wws.lanzous.com/b01hh31id', dir_pwd='./download/lanzou')
    # downer.down_dir_by_url('https://wws.lanzous.com/b01hh63kf', dir_pwd='./download/lanzou')
    downer.down_dir_by_url('https://wws.lanzous.com/b01hh2zve', dir_pwd='./download/lanzou')
    #


def example4():
    downer.upload_file('/Users/liangtaoniu/workspace/dataset/tianchi001/trainset.zip', folder_id=2010460)
    downer.upload_file('/Users/liangtaoniu/workspace/dataset/tianchi001/test_input.zip', folder_id=2010460)


def example5():
    print(downer.get_dir_list(folder_id=2010460))


example4()
# example2()
example3()
