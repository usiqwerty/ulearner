import re

import cached_requests
from ulearn.config import UlearnConfig
from ulearn.pages.exercise import parse_exercise
from ulearn.pages.homework import parse_homework
from ulearn.pages.lesson import parse_lesson
from ulearn.pages.page import UlearnPage
from ulearn.pages.theory_task import parse_theory_task_html
from ulearn.utils import extract_blocks


def parse_page(page_id: str, config: UlearnConfig, force_page_type: str | None = None) -> UlearnPage:
    page_type = force_page_type or config.course.get_page_type(page_id)
    if page_type == 'quiz':
        slug = config.course.get_slug_by_id(page_id)
        url = f"https://ulearn.me/course/{config.course.code}/{slug}"
        r = cached_requests.get(url)
        return parse_theory_task_html(r.text)
    else:
        url = f"https://api.ulearn.me/slides/{config.course.code}/{page_id}"
        r = cached_requests.get(url)
        data = r.json()
        if data.get('status') == 'error':
            raise Exception(data['message'])
        blocks = extract_blocks(data['blocks'])

        if page_type == "lesson":
            return parse_lesson(blocks, page_id, data['title'], config)
        elif page_type == "exercise":
            return parse_exercise(blocks)
        elif page_type == "homework":
            return parse_homework(blocks)
        else:
            raise Exception("Не удалось определить тип страницы")


def parse_link(url: str):
    """Извлечь ID курса и ID страницы из ссылки на эту страницу"""
    r = re.search(r"https://ulearn.me/[Cc]ourse/([\w\d-]+)/[\w_]+_([\d\w\-]+)", url)
    course_id, pid = r.groups()
    return course_id.lower(), pid
