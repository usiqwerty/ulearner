import file_manager.explorer
from appconfig import user_id
from cached_requests import save_to_disk
from ulearn.config import UlearnConfig
from ulearn.courses.manager import get_course
from ulearn.parser import parse_page

# TODO: здесь же устанавливать рабочий каталог для homework
# и прокинуть туда config

pid = "f9280ba1-a218-4213-bc9c-715f6cb45fc4"
course_id = "basicprogramming2"

print("Project root:", file_manager.explorer.project_root)

course = get_course(course_id)
config = UlearnConfig(course, user_id)
r = parse_page(pid, config)
print(r.generate_prompt())
# resp = request(r.generate_prompt())
#
# print(resp)

save_to_disk()
