import json
import os.path
config_fn = os.path.join("userdata", "config.json")

try:

    with open(config_fn, encoding="utf-8") as f:
        config_data = json.load(f)
    user_id = config_data['ulearn_uid']
    openai_api_key = config_data['openai_api_key']
    ya300_apikey = config_data['ya300_apikey']
    yandex_session_cookie = config_data['yandex_session_cookie']
    ys_cookie = config_data['ys_cookie']
    ulearner_root = config_data['ulearner_root']
except (KeyError, FileNotFoundError) as e:
    print(e)
    print('{"ulearner_root": "", "ulearn_uid": "", "openai_api_key": "", "ya300_apikey": "", "yandex_session_cookie": "", "ys_cookie": ""}')
    exit(1)

