import json
from dataclasses import dataclass
from typing import Any

import requests

filename = "userdata/cache.json"
try:
    with open(filename, encoding='utf-8') as f:
        cache: dict[str, Any] = json.load(f)
except FileNotFoundError:
    cache: dict[str, Any] = {}
cache_changed = False


@dataclass
class FakeResponse:
    text: str

    def json(self):
        return json.loads(self.text)


def get(url: str, force_update=False, **kwargs):
    global cache_changed
    if url not in cache or force_update:
        print(f"[WEB] {url}")
        response = requests.get(url, **kwargs)
        cache[url] = response.text
        cache_changed = True
    return FakeResponse(cache[url])


def save_to_disk():
    if cache_changed:
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump(cache, fp)
        print('Cache saved')

    else:
        print('Cache has not changed')
