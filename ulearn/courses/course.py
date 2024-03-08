from typing import NamedTuple

from pydantic import BaseModel


class Slide(BaseModel):
    slide_id: str
    slug: str
    slide_type: str
    title: str


class CourseUnit(BaseModel):
    unit_id: str
    slides: list[Slide]


class UlearnCourse(BaseModel):
    name: str
    code: str
    lecture_prompt: str
    units: list[CourseUnit]

    def get_slug_by_id(self, page_id):
        for unit in self.units:
            for slide in unit.slides:
                if slide.slide_id == page_id:
                    return slide.slug

    def get_page_type(self, page_id: str):
        """Возвращает тип страницы"""
        for unit in self.units:
            for slide in unit.slides:
                if slide.slide_id == page_id:
                    if slide.slide_type == "autocheck":
                        return "homework"
                    return slide.slide_type


SlideProgress = NamedTuple('SlideProgress', [('id', str), ('score', str), ('visited', bool), ('skipped', bool)])




