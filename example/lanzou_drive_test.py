from notedrive.lanzou import LanZouCloud

lzy = LanZouCloud()

print(lzy.login_by_cookie() == LanZouCloud.SUCCESS)
