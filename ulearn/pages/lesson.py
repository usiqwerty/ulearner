from dataclasses import dataclass

from ulearn.config import UlearnConfig
from ulearn.pages.comment import Comment, get_comments
from ulearn.pages.page import UlearnPage


@dataclass
class LecturePage(UlearnPage):
    name: str
    timecodes: dict[str, str]
    code_block: str
    comments: list[Comment]
    config: UlearnConfig
    video_id: str

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
{self.code_block or ""}
```

Можешь объяснить эту тему? Изложи суть и проиллюстрируй примерами кода. Наверняка приведённая информация устарела или неточна, если это так, можешь исправить эти неточности"""


# Возможно, комментарии под лекцией помогут выделить проблемные места:
# {comments_textual}

def parse_lesson(blocks: dict[str, dict], page_id, title, config: UlearnConfig):
    video = blocks.get('video') or blocks.get('youtube')
    code_block = blocks.get('code')

    # if not code_block:
    #     raise Exception('В лекции нет блока с кодом')
    video_id = video['videoId']
    annotation = video['annotation']
    fragments = annotation['fragments']
    timecodes = {}
    for frag in fragments:
        timecodes[frag['offset']] = frag['text']
    code_conspect = code_block['code'] if code_block else None
    comments = get_comments(page_id, config.course.code)
    return LecturePage(title, timecodes, code_conspect, comments, config, video_id)
