import os.path

import requests.auth

auth_fn = os.path.join("userdata", "auth.cookie")

try:
    with open(auth_fn, encoding='utf-8') as f:
        auth_cookie = f.read()
except FileNotFoundError:
    print(f'Сохраните значение куки авторизации в файле {auth_fn}')
    exit(1)

ulearn_cookies = {'ulearn.auth': auth_cookie}
ulearn_auth_token = None


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = f"Bearer {self.token}"
        return r


def fetch_token():
    global ulearn_auth_token
    print('Fetching token')
    r_tok = post_authenticated("https://api.ulearn.me/account/token")
    r_tok_json = r_tok.json()
    ulearn_auth_token = r_tok_json['token']
    print(f"Token ready: {ulearn_auth_token}")


def post_authenticated(url, with_token=False):
    auth_method = None
    if with_token:
        auth_method = BearerAuth(ulearn_auth_token)
    return requests.post(url,
                         cookies=ulearn_cookies,
                         auth=auth_method,
                         headers={'content-type': 'application/json',
                                  'Sec-Fetch-Dest': "empty",
                                  'Origin': 'https://ulearn.me',
                                  "Referer": "https://ulearn.me/",
                                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
                                  },
                         data="{}"
                         )
