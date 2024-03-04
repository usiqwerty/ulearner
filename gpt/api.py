import json
import os.path
import random

import httpx
from openai import OpenAI, APIConnectionError, PermissionDeniedError

from appconfig import openai_api_key

proxies_fn = os.path.join("userdata", "proxies.json")
VPN_MODE = False
http_proxy_client = None

if not VPN_MODE:
    with open(proxies_fn) as fp:
        proxies: list[str] = json.load(fp)
    print(f"{len(proxies)} proxies left")
    proxy_ip = random.choice(proxies)
    # noinspection HttpUrlsUsage
    proxy_url = "http://" + proxy_ip
    http_proxy_client = httpx.Client(proxy=proxy_url)

client = OpenAI(api_key=openai_api_key, http_client=http_proxy_client)


def request(query: str):
    """Ответ от ChatGPT"""
    msgs = [
        {"role": "user", "content": query}
    ]
    try:
        chat_completion = client.chat.completions.create(messages=msgs, model="gpt-3.5-turbo", temperature=0.2)
        return chat_completion.choices[0].message.content
    except (APIConnectionError, PermissionDeniedError) as e:
        if not VPN_MODE:
            proxies.remove(proxy_ip)
            with open(proxies_fn, 'w') as f:
                json.dump(proxies, f)
            print('Proxy removed from list')
        print(e)


def stream_request(query: str):
    msgs = [
        {"role": "user", "content": query}
    ]
    stream = client.chat.completions.create(messages=msgs, model="gpt-3.5-turbo", stream=True)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

    return stream.response.content
