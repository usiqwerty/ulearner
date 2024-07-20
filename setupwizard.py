import json
import os.path

import requests
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder

from ulearn.web import fetch_token, get_authenticated


def full_setup(path: str, config_fn: str, auth_cookie_fn: str):
    print("Начинаем настройку ulearner")
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Создана директория: {path}")
    config_data = {
        'ulearn_uid': get_user_id(auth_cookie_fn),
        'openai_api_key': input("Введите API ключ для OpenAI. Enter, чтобы пропустить: "),
        'ulearner_root': input("Введите папку, в которую будут скачиваться файлы: ")
    }
    with open(config_fn, 'w', encoding='utf-8') as f:
        json.dump(config_data, f)
        print(f"Конфигурация сохранена: {config_fn}")


def get_auth_cookie(auth_cookie_fn: str):
    login_url = 'https://ulearn.me/Login?ReturnUrl=/'
    login_page_response = requests.get("https://ulearn.me/login")
    login_page = login_page_response.text
    anti_forgery_cookies = login_page_response.cookies.get_dict()
    soup = BeautifulSoup(login_page, 'html.parser')

    request_verification_token = soup.find(attrs={"name": "__RequestVerificationToken"})['value']

    print("Введите данные для авторизации на Ulearn")
    username = input("Логин: ")
    password = input("Пароль: ")
    fields = {
        "UserName": username,
        "Password": password,
        "RememberMe": "true",
        "__RequestVerificationToken": request_verification_token
    }

    # Я не знаю, что значат эти цифры и откуда они берутся
    # И да, почему тут так много чёрточек...
    data = MultipartEncoder(fields, boundary="---------------------------20425708503272018662337569183")
    headers = {
        "referer": "https://ulearn.me/login?returnUrl=%2F",
        "Content-Type": data.content_type,
        "Origin": "https://ulearn.me",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.1"
    }
    r = requests.post(login_url, headers=headers, data=data.to_string(), cookies=anti_forgery_cookies)
    auth_cookie = r.history[0].cookies['ulearn.auth']

    with open(auth_cookie_fn, 'w', encoding='utf-8') as f:
        f.write(auth_cookie)
        print(f"Cookie сохранён: {auth_cookie_fn}")
    return auth_cookie


def get_user_id(auth_cookie_fn: str):
    auth_cookie = get_auth_cookie(auth_cookie_fn)
    auth_token = fetch_token(auth_cookie)
    r = get_authenticated("https://api.ulearn.me/account", auth_token, auth_cookie, True)
    userdata = r.json()['user']

    user_id = userdata['id']
    user_name = userdata['firstName']
    user_gender = userdata['gender']
    match user_gender:
        case "male":
            translated_gender = "мужчина"
        case "female":
            translated_gender = "женщина"
        case _:
            # ну вот мне просто интересно, они сделали текстовое поле,
            # как будто собираются хранить там небинарные значения
            translated_gender = user_gender
    if translated_gender == user_gender:
        print(f"Ulearn сказал, что вас зовут {user_name} и что ваш пол {translated_gender}. Так держать!")
    else:
        print(f"Ulearn сказал, что вас зовут {user_name} и что вы {translated_gender}. Так держать!")

    return user_id
