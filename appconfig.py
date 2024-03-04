import json
import os.path
config_fn = os.path.join("userdata", "config.json")

try:

    with open(config_fn) as f:
        config_data = json.load(f)
    user_id = config_data['ulearn_uid']
    openai_api_key = config_data['openai_api_key']
    ya300_apikey = config_data['ya300_apikey']
    yandex_session_cookie = config_data['yandex_session_cookie']
    ys_cookie = config_data['ys_cookie']
except (KeyError, FileNotFoundError) as e:
    print(e)
    print('{"ulearn_uid":ULEARN_UID, "openai_api_key":OPENAI_API_KEY}')
    exit(1)
