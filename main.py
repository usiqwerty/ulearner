import faulthandler

import openai

from appconfig import user_id
from cached_requests import save_to_disk
from ulearn.config import UlearnConfig
from ulearn.courses.manager import get_course
from ulearn.parser import parse_page, parse_link
from gpt.api import request
faulthandler.enable()

url = "https://ulearn.me/course/basicprogramming2/Praktika_Potok_dlya_AI__3a12764a-146f-1b7d-b184-a35b852d0351"

course_id, pid = parse_link(url)


course = get_course(course_id)
config = UlearnConfig(course, user_id)
r = parse_page(pid, config)

# print(r.generate_prompt())


try:
    resp = request(r.generate_prompt(), r.system_message)
    print(resp)
except openai.RateLimitError as e:
    print(f"{e.status_code} - {e.type}")
    print(e.body['message'])

save_to_disk()
