from notedrive.lanzou import LanZouCloud, CodeDetail, download

downer = LanZouCloud()
downer.ignore_limits()

downer.login_by_cookie()


def example1():
    print(downer.login_by_cookie() == CodeDetail.SUCCESS)


def example2():
    file_path = '/Users/liangtaoniu/workspace/MyDiary/tmp/weights/yolov3.weight'
    downer.upload_file(file_path=file_path)


def example3():
    download('https://wws.lanzous.com/b01hjn3aj', dir_pwd='./download/lanzou')
    # download('https://wws.lanzous.com/b01hh63kf', dir_pwd='./download/lanzou')
    # downer.down_dir_by_url('https://wws.lanzous.com/b01hh2zve', dir_pwd='./download/lanzou')

    pass


def example4():
    print("upload")
    # downer.upload_file('/Users/liangtaoniu/workspace/MyDiary/tmp/models/yolo/configs/yolov3.h5', folder_id=2129808)
    # downer.upload_file('/Users/liangtaoniu/workspace/MyDiary/tmp/models/yolo/configs/yolov3.weights', folder_id=2129808)
    # downer.upload_file('/Users/liangtaoniu/workspace/dataset/models/yolov4.weights', folder_id=2129808)
    res = downer.upload_file('/Users/liangtaoniu/workspace/dataset/models/annotations_trainval2017.zip',
                             folder_id=2160967)
    res = downer.upload_file('/Users/liangtaoniu/workspace/dataset/models/val2017.zip', folder_id=2160967)

    print(res)
    pass


def example5():
    print(downer.get_dir_list(folder_id=2160967))
    

# example1()
# example3()
example4()
# example2()
example5()
# https://wws.lanzous.com/b01hjn3aj
