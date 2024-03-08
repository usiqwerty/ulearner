import datetime
from dataclasses import dataclass

import cached_requests


@dataclass
class Comment:
    author: str
    publish_time: datetime.datetime
    text: str
    likes: int
    fold_level: int
    replies: list

    def __str__(self):
        self.text = self.text.replace('\n', '')
        if self.fold_level:
            return f"Ответ: [{self.author} - {self.likes} лайков]: {self.text}"
        else:
            return f"[{self.author} - {self.likes} лайков]: {self.text}"


def get_comments(page_id: str, course_id: str) -> list[Comment]:
    url = f"https://api.ulearn.me/comments?courseId={course_id}&slideId={page_id}&forInstructors=false"
    r = cached_requests.get(url)
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
