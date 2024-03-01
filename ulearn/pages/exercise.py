from dataclasses import dataclass

from bs4 import BeautifulSoup as bs

from ulearn.pages.page import UlearnPage


@dataclass
class ExercisePage(UlearnPage):
	introduction: str
	main_code: str
	initial_code: str

	def generate_prompt(self) -> str:
		return '\n'.join([self.introduction, self.main_code, "Вот код, который нужно дополнить:", self.initial_code])


def parse_exercise(blocks):
	task = bs(blocks['html']["content"], 'html.parser').text
	task_sample_code = blocks['code']["code"]
	code_block = blocks['exercise']['exerciseInitialCode']

	page = ExercisePage(introduction=task, main_code=task_sample_code, initial_code=code_block)
	return page
