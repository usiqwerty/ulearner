from dataclasses import dataclass

from bs4 import BeautifulSoup as bs
from file_manager.explorer import get_code_file
from file_manager.explorer import get_requested_file_name
from sharp_parser.oop.classes import CSharpClass
from ulearn.pages.page import UlearnPage
from ulearn.project.manager import extract_project_name
from ulearn.project.dependencies import resolve_all_dependencies

code_quality_note = '\n'.join([
    "Не забывай о правилах написания чистого кода, а так же используй var при объявлении типов переменных.",
    "Тесты писать не нужно, т.к. они уже есть в проверяющей системе.",
])


@dataclass
class HomeworkPage(UlearnPage):
    prelude: str
    initial_code_file: str
    project_dependencies: list[CSharpClass]

    def generate_prompt(self) -> str:
        if not self.initial_code_file:
            return self.prelude + "Вставьте содержимое вашего файла:"
        depline = f"```\n{'\n'.join(str(x) for x in self.project_dependencies)}\n```\n" if self.project_dependencies else ""

        return (self.prelude + "\n\n" +
                "Вот сигнатуры классов, объявленных в других файлах проекта, которые могут использоваться в коде:\n" +
                depline +
                code_quality_note + "\nКод, который тебе нужно дополнить:\n"  "```\n"+
                self.initial_code_file+"```")


def parse_homework(blocks: dict[str, list[dict]]):
    task_blocks = blocks['html']
    initial_content = blocks['exercise'][0]['exerciseInitialCode'].replace('\n', '')
    code_file_name = get_requested_file_name(initial_content)

    content = bs(''.join(x['content'] for x in task_blocks), "html.parser")
    project = ""
    project_link = ""
    for a_tag in content.find_all('a'):
        project_link: str = a_tag['href']
        if project_link.endswith('.zip'):
            project = extract_project_name(project_link)
            break
        a_tag.decompose()
    if not project:
        raise Exception("No project")

    prelude = content.text
    main_source = get_code_file(project, code_file_name, project_link)
    if main_source:
        deps = resolve_all_dependencies(main_source, project)
    else:
        deps = []

    page = HomeworkPage(prelude=prelude, initial_code_file=main_source, project_dependencies=deps)
    return page
