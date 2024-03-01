import json
import os.path
config_fn = os.path.join("userdata", "config.json")

try:

    with open(config_fn) as f:
        config_data = json.load(f)
    user_id = config_data['ulearn_uid']
    openai_api_key = config_data['openai_api_key']
except (KeyError, FileNotFoundError) as e:
    print(e)
    print('{"ulearn_uid":ULEARN_UID, "openai_api_key":OPENAI_API_KEY}')
    exit(1)
