import json
import os.path

from setupwizard import full_setup

userdata_dir ="userdata"
config_fn = os.path.join(userdata_dir, "config.json")
auth_cookie_fn = os.path.join(userdata_dir, "auth.cookie")
error_count = 0
try:
    with open(config_fn, encoding="utf-8") as f:
        config_data: dict = json.load(f)
    user_id = config_data.get('ulearn_uid')
    openai_api_key = config_data.get('openai_api_key')
    # ya300_apikey = config_data.get('ya300_apikey')
    yandex_session_cookie = config_data.get('yandex_session_cookie')
    ys_cookie = config_data.get('ys_cookie')
    ulearner_root = config_data.get('ulearner_root')

    if not user_id:
        print("В конфигурации по ключу user_id укажите id пользователя на Ulearn")
    if not openai_api_key:
        print("Не указан API ключ OpenAI, работаем без него")
    if not ulearner_root:
        print("В конфигурации по ключу ulearner_root уажите полный путь к папке, где будем хранить файлы")

except FileNotFoundError as e:
    print(f"Не найден файл конфигурации {config_fn}")
    error_count += 1

try:
    with open(auth_cookie_fn, encoding='utf-8') as f:
        auth_cookie = f.read()
except FileNotFoundError:
    print(f'Не найден куки авторизации: {auth_cookie_fn}')
    error_count += 1

if error_count == 2:
    full_setup(userdata_dir, config_fn, auth_cookie_fn)
    print("Настройка завершена, запустите ulearner ещё раз, чтобы начать")
    exit(1)
elif error_count:
    exit(1)
