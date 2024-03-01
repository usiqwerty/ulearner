import json
import os.path

from ulearn.courses.course import SlideProgress, UlearnCourse

filename = os.path.join("userdata", "courses.json")
progress_fn = os.path.join("userdata", 'progress.json')


def load_courses() -> dict[str, UlearnCourse]:
    try:
        with open(filename, encoding='utf-8') as fp:
            courses = {k: UlearnCourse(**v) for k, v in json.load(fp).items()}
    except FileNotFoundError:
        print('No courses saved')
        courses = {}
    return courses


def save_courses(data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)
        print(f"Written {filename}")


def load_progress() -> list[SlideProgress]:
    try:
        with open(progress_fn, encoding='utf-8') as fp:
            progress = [SlideProgress(*x) for x in json.load(fp)]
    except FileNotFoundError:
        print('No progress saved')
        progress = []
    return progress


def save_progress(data):
    with open(progress_fn, 'w', encoding='utf-8') as f:
        json.dump(data, f)
        print(f"Written {progress_fn}")
