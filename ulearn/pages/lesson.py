import datetime
from dataclasses import dataclass

import requests

from ulearn.config import UlearnConfig
from ulearn.pages.page import UlearnPage


@dataclass
class Comment:
    author: str
    publish_time: datetime.datetime
    text: str
    likes: int
    fold_level: int
    replies: list

    def __str__(self):
        return f"{' * ' * self.fold_level}[{self.author} - {self.likes} лайков] {self.text}"


@dataclass
class LecturePage(UlearnPage):
    name: str
    timecodes: dict[str, str]
    code_block: str
    comments: list[Comment]
    config: UlearnConfig

    def generate_prompt(self) -> str:
        timecodes_textual = ""
        for k, v in self.timecodes.items():
            timecodes_textual += f"{k}: {v}\n"

        comments_textual = ""
        for comment in self.comments:
            comments_textual += str(comment) + "\n"
            for reply in comment.replies:
                comments_textual += str(reply) + "\n"
        return f"""Вот конспект видеолекции по {self.config.course.lecture_prompt} на тему {self.name}:
{timecodes_textual}
```
{self.code_block}
```

Можешь объяснить эту тему? Изложи суть и проиллюстрируй примерами кода. Наверняка приведённая информация устарела или неточна, если это так, можешь исправить эти неточности"""


# Возможно, комментарии под лекцией помогут выделить проблемные места:
# {comments_textual}

def parse_lesson(blocks: dict[str, dict], page_id, title, config: UlearnConfig):
    video = blocks.get('video') or blocks.get('youtube')
    code_block = blocks['code']

    if not code_block:
        raise Exception('В лекции нет блока с кодом')

    annotation = video['annotation']
    fragments = annotation['fragments']
    timecodes = {}
    for frag in fragments:
        timecodes[frag['offset']] = frag['text']
    page = LecturePage(title, timecodes, code_block['code'], get_comments(page_id, config.course.code), config)
    return page


def get_comments(page_id: str, course_id: str) -> list[Comment]:
    url = f"https://api.ulearn.me/comments?courseId={course_id}&slideId={page_id}&forInstructors=false"
    r = requests.get(url)
    data = r.json()

    comments = []

    for comment in data['topLevelComments']:
        comment_cleaned = Comment(comment['author']['visibleName'],
                                  datetime.datetime.fromisoformat(comment['publishTime']),
                                  comment['text'], comment['likesCount'], 0, [])
        for reply in comment['replies']:
            repl = Comment(reply['author']['visibleName'], datetime.datetime.fromisoformat(reply['publishTime']),
                           reply['text'], int(reply['likesCount']), 1, [])
            comment_cleaned.replies.append(repl)
        comments.append(comment_cleaned)
    return comments
