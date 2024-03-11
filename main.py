import faulthandler

from appconfig import user_id
from cached_requests import save_to_disk
from ulearn.config import UlearnConfig
from ulearn.courses.manager import get_course
from ulearn.parser import parse_page, parse_link
from gpt.api import request
from ulearn.project.manager import download_and_unzip
faulthandler.enable()
# TODO: здесь же устанавливать рабочий каталог для homework
# и прокинуть туда config
url = "https://ulearn.me/course/nand2tetris/Zadacha_CodeWriter_6b7304b6-8de1-49a5-8506-d32b68a68b39"

course_id, pid = parse_link(url)


course = get_course(course_id)
config = UlearnConfig(course, user_id)
r = parse_page(pid, config)

# print(r.system_message)
# print(r.generate_prompt())


# resp = request(r.generate_prompt(), r.system_message)
# print(resp)

save_to_disk()
