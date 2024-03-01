from dataclasses import dataclass

from ulearn.courses.course import UlearnCourse


@dataclass
class UlearnConfig:
    course: UlearnCourse
    user_id: str
