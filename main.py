import file_manager.explorer
from appconfig import user_id
from cached_requests import save_to_disk
from ulearn.config import UlearnConfig
from ulearn.courses.manager import get_course
from ulearn.parser import parse_page, parse_link
from gpt.api import request
# TODO: здесь же устанавливать рабочий каталог для homework
# и прокинуть туда config
course_id, pid = parse_link('https://ulearn.me/course/nand2tetris/Zadacha_Parser_e616a714-9ecc-4b46-a04c-85a6ce3b9d55')

print("Project root:", file_manager.explorer.project_root)

course = get_course(course_id)
config = UlearnConfig(course, user_id)
r = parse_page(pid, config, force_page_type="homework")
print(r)
resp = request(r.generate_prompt())

print(resp)

save_to_disk()
