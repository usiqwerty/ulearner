import requests.auth


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = f"Bearer {self.token}"
        return r


def fetch_token(auth_cookie):
    print('Fetching token')
    r_tok = post_authenticated("https://api.ulearn.me/account/token", "", auth_cookie, False)
    r_tok_json = r_tok.json()
    ulearn_auth_token = r_tok_json['token']
    print(f"Token ready: {ulearn_auth_token}")
    return ulearn_auth_token


def post_authenticated(url, ulearn_auth_token, auth_cookie, with_token):
    auth_method = None
    if with_token:
        auth_method = BearerAuth(ulearn_auth_token)
    return requests.post(url,
                         cookies={'ulearn.auth': auth_cookie},
                         auth=auth_method,
                         headers={'content-type': 'application/json',
                                  'Sec-Fetch-Dest': "empty",
                                  'Origin': 'https://ulearn.me',
                                  "Referer": "https://ulearn.me/",
                                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
                                  },
                         data="{}"
                         )


def get_authenticated(url, ulearn_auth_token, auth_cookie, with_token):
    auth_method = None
    if with_token:
        auth_method = BearerAuth(ulearn_auth_token)
    return requests.get(url,
                        cookies={'ulearn.auth': auth_cookie},
                        auth=auth_method,
                        headers={'content-type': 'application/json',
                                 'Sec-Fetch-Dest': "empty",
                                 'Origin': 'https://ulearn.me',
                                 "Referer": "https://ulearn.me/",
                                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
                                 },
                        )
