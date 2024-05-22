import json
import os.path
config_fn = os.path.join("userdata", "config.json")

try:
    with open(config_fn, encoding="utf-8") as f:
        config_data:dict = json.load(f)
    user_id = config_data.get('ulearn_uid')
    openai_api_key = config_data.get('openai_api_key')
    # ya300_apikey = config_data.get('ya300_apikey')
    yandex_session_cookie = config_data.get('yandex_session_cookie')
    ys_cookie = config_data.get('ys_cookie')
    ulearner_root = config_data.get('ulearner_root')
except FileNotFoundError as e:
    print(e)
    print(f"Создайте файл конфигурации {config_fn}")
    exit(1)

if not user_id:
    print("В конфигурации по ключу user_id укажите id пользователя на Ulearn")
if not openai_api_key:
    print("Не указан API ключ OpenAI, работаем без него")
if not ulearner_root:
    print("В конфигурации по ключу ulearner_root уажите полный путь к папке, где будем хранить файлы")