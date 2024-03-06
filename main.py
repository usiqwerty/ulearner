import file_manager.explorer
from appconfig import user_id
from cached_requests import save_to_disk
from ulearn.config import UlearnConfig
from ulearn.courses.manager import get_course
from ulearn.parser import parse_page, parse_link
from gpt.api import request
from ya300 import video_summary
# TODO: здесь же устанавливать рабочий каталог для homework
# и прокинуть туда config
course_id, pid = parse_link("https://ulearn.me/course/basicprogramming2/Poisk_podstroki_v_stroke_2_d9c61ebc-527a-4311-b9b8-7b9e5b7f9100")

print("Project root:", file_manager.explorer.project_root)

course = get_course(course_id)
config = UlearnConfig(course, user_id)
r = parse_page(pid, config)

#video_summary(r.video_id)
# print(r.generate_prompt())


resp = request(r.generate_prompt())
print(resp)

save_to_disk()
