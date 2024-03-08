import requests

from ulearn.courses.course import UlearnCourse, CourseUnit, Slide
from ulearn.courses.storage import load_courses, save_courses


def fetch_course_full(course_id: str) -> UlearnCourse:
    """Скачать, распарсить и сохранить информацию по курсу: юниты, слайды"""
    global courses
    url = f"https://api.ulearn.me/courses/{course_id}"
    r = requests.get(url)
    data = r.json()
    course_name = data['title']

    course_units = []

    for unit in data['units']:
        the_unit = CourseUnit(unit_id=unit['id'], slides=[])

        for slide in unit['slides']:
            if slide['type'] == 'exercise':
                sl_type = slide['scoringGroup']
            else:
                sl_type = slide['type']
            the_slide = Slide(slide_id=slide['id'], slug=slide['slug'], slide_type=sl_type, title=slide['title'])
            the_unit.slides.append(the_slide)
        course_units.append(the_unit)
    lp = input("lecture_prompt: ")
    course = UlearnCourse(name=course_name, code=course_id, lecture_prompt=lp, units=course_units)

    courses[course_id] = course  # .json()  # asdict(course)
    save_courses(courses)
    return course


courses = load_courses()
print('units done')


def get_course(course_id: str) -> UlearnCourse:
    if course_id not in courses:
        fetch_course_full(course_id)
    return courses[course_id]

#
# def fetch_online_user_progress(course_id: str):
#     """Скачать, распасить, сохранить прогресс"""
#     url = f'https://api.ulearn.me/user-progress/{course_id}'
#     fetch_token()
#     data = post_authenticated(url, with_token=True)
#     print(data, data.text)
#     r = data.json()
#     user_progress = r['userProgress'][user_id]
#     local_progress = []
#     for visited_slide_id, visited_slide in user_progress['visitedSlides'].items():
#         local_progress.append(
#             SlideProgress(visited_slide_id, visited_slide['score'], visited_slide['visited'],
#                           visited_slide['isSkipped'])
#         )
#     save_progress(local_progress)
#     return local_progress
