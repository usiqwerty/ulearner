import faulthandler

import openai

from appconfig import user_id, openai_api_key
from cached_requests import save_to_disk
from ulearn.config import UlearnConfig
from ulearn.courses.manager import get_course
from ulearn.parser import parse_page, parse_link
from gpt.api import request
faulthandler.enable()

url = "https://ulearn.me/course/basicprogramming2/Praktika_Dokumentatsiya__d6e4df45-0a2f-47c9-ad6d-19cc69e9c549"

course_id, pid = parse_link(url)
course = get_course(course_id)
config = UlearnConfig(course, user_id)
r = parse_page(pid, config)

if openai_api_key:
    try:
        resp = request(r.generate_prompt(), r.system_message)
        print(resp)
    except openai.RateLimitError as e:
        print(f"{e.status_code} - {e.type}")
        print(e.body['message'])
else:
    print(r.generate_prompt())
save_to_disk()
