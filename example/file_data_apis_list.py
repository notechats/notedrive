from notedrive.baidu._token import AccessToken

token = AccessToken(api_key='DmDvl0rVkYGOLu8rN6RgdWMk', secret_key='gP9mLdtrmvRKYEKhtjEdSRKewkDOHnKf')
# token = AccessToken()
# token.init_refresh_token()
token.refresh_access_token()
print("access_token\t" + token.secret['token']['access_token'])
