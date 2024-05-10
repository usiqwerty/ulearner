from dataclasses import dataclass

from bs4 import BeautifulSoup as bs

from ulearn.pages.page import UlearnPage
from ulearn.utils import letter_index


@dataclass
class TheoryTaskPage(UlearnPage):
	content: str

	def generate_prompt(self) -> str:
		# "Напиши ответы к заданиям: \n" +
		# "Ты профессиональный программист на C#. Выполни указанные задания\n" +
		return "Выполни задания и напиши правильные ответы:\n"+self.content


def parse_theory_task_html(page_html: str):
	soup = bs(page_html, "html.parser").find(class_="quiz__blocks")
	textual_content = ""
	for question_block in soup.children:
		if question_block.name == "div":
			title_tag = question_block.find(class_="quiz-block__text")
			answer_tags = question_block.find_all(class_="quiz")
			question = title_tag.text.strip().replace('\n', '')
			textual_content += question + "\n"
			for i, answer_tag in enumerate(answer_tags):
				answer = answer_tag.text.strip().replace('\n', '')
				textual_content += f"{letter_index(i)}. {answer}" + '\n'
		else:
			textual_content += question_block.text.strip() + '\n'
	return TheoryTaskPage(textual_content)
