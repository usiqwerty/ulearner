from dataclasses import dataclass

from ulearn.config import UlearnConfig
from ulearn.pages.comment import Comment, get_comments
from ulearn.pages.page import UlearnPage


@dataclass
class LecturePage(UlearnPage):
    name: str
    timecodes: dict[str, str] | None
    code_block: str
    comments: list[Comment]
    config: UlearnConfig
    video_id: str

    def generate_prompt(self) -> str:


        comments_textual = ""
        for comment in self.comments:
            comments_textual += str(comment) + "\n"
            for reply in comment.replies:
                comments_textual += str(reply) + "\n"

        if not self.timecodes and not self.code_block:
            prompt = f"Нужен конспект видеолекции по {self.config.course.lecture_prompt} на тему {self.name}.\n"
        else:

            prompt = f"Вот конспект видеолекции по {self.config.course.lecture_prompt} на тему {self.name}:\n"

            if self.timecodes:
                timecodes_textual = ""
                for k, v in self.timecodes.items():
                    timecodes_textual += f"{k}: {v}\n"
                prompt += timecodes_textual + "\n"
            if self.code_block:
                prompt += f"```\n{self.code_block or ""}\n```\n"

        prompt += ("Можешь объяснить эту тему? "
                "Раскрой содержание и проиллюстрируй примерами кода. "
                "Наверняка приведённая информация устарела или неточна, если это так, можешь исправить эти неточности. "
                "Возможно, комментарии пользователей помогут выявить важные моменты:\n" +
                comments_textual)
        return prompt


def parse_lesson(blocks: dict[str, list[dict]], page_id, title, config: UlearnConfig):
    video_blocks = blocks.get('video') or blocks.get('youtube')
    timecodes = {}
    video_id = None
    code_blocks = blocks.get('code')

    # if not code_blocks:
    #     raise Exception('В лекции нет блока с кодом')
    if video_blocks:
        video = video_blocks[0]
        video_id = video['videoId']

        annotation = video['annotation']
        if annotation is not None:
            fragments = annotation['fragments']

            for frag in fragments:
                timecodes[frag['offset']] = frag['text']
        else:
            timecodes = None

    code_conspect = code_blocks[0]['code'] if code_blocks else None
    comments = get_comments(page_id, config.course.code)
    return LecturePage(title, timecodes, code_conspect, comments, config, video_id)
