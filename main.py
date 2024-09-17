import faulthandler

import openai

from appconfig import user_id, openai_api_key
from cached_requests import save_to_disk
from ulearn.config import UlearnConfig
from ulearn.courses.manager import get_course
from ulearn.parser import parse_page, parse_link
from gpt.api import request
faulthandler.enable()

url = "https://ulearn.me/course/cs2/Poryadok_initsializatsii_a530d860-f05b-485d-b20b-7733573faea8"

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
