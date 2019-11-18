from notedrive.baidu.token_ import AccessToken

token = AccessToken()
# token = AccessToken()
# token.init_refresh_token()
token.refresh_access_token()
print("access_token\t" + token.secret['token']['access_token'])
