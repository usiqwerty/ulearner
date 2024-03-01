import file_manager.explorer
from appconfig import user_id
from cached_requests import save_to_disk
from ulearn.config import UlearnConfig
from ulearn.courses.manager import get_course
from ulearn.parser import parse_page, parse_link
from gpt.api import request
# TODO: здесь же устанавливать рабочий каталог для homework
# и прокинуть туда config
course_id, pid = parse_link('https://ulearn.me/course/basicprogramming2/Steki_i_ocheredi_0b1faf5b-7082-4a99-8556-f5b4c00bd912')

print("Project root:", file_manager.explorer.project_root)

course = get_course(course_id)
config = UlearnConfig(course, user_id)
r = parse_page(pid, config)
print(r)
resp = request(r.generate_prompt())

print(resp)

save_to_disk()
