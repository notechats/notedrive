import hashlib
import os


def parse_path(yun_path, loc_path=None, isdir=True):
    cwd = os.getcwd()

    def last_dir(path):
        if path is None:
            return 'default'
        p1, p2 = os.path.split(path)
        if p2 == '':
            return os.path.split(p1)[-1]
        else:
            return p2

    if isdir:
        if loc_path is None:
            loc_path = '{}/{}'.format(cwd, last_dir(yun_path))
        elif loc_path[0] != '/':
            loc_path = '{}/{}'.format(cwd, loc_path)

    else:
        yun_dir, yun_filename = os.path.split(yun_path)

        # 空路径，保存到当前文件夹下
        if loc_path is None:
            loc_path = '{}/{}'.format(cwd, yun_filename)
        else:
            loc_dir, loc_filename = os.path.split(loc_path)

            if loc_dir is None or loc_dir == '':
                loc_dir = cwd
            # 相对路径，前面补上全路径
            elif loc_dir[0] != '/':
                loc_dir = '{}/{}'.format(cwd, loc_dir)

            # 没有设置文件名，取默认文件名
            if loc_filename == '':
                loc_filename = yun_filename

            loc_path = os.path.join(loc_dir, loc_filename)
    return yun_path, loc_path


print(parse_path('/a', 'test'))
print(parse_path('/a', 'test/', isdir=False))
print(parse_path('/a.txt'))
print(parse_path('/a/'))


def get_file_md5(path):
    m = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            data = f.read(1024 * 4)
            if not data:
                break
            m.update(data)

    return m.hexdigest()


file_name = "test2.txt"
file_md5 = get_file_md5(file_name)
print(file_md5)
