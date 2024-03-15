from dataclasses import dataclass

from bs4 import BeautifulSoup as bs
from file_manager.explorer import get_code_file
from file_manager.explorer import get_requested_file_name
from sharp_parser.classes import CSharpClass
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
        return (self.prelude + "\n\n" +
                "Вот сигнатуры классов, объявленных в других файлах проекта, которые могут использоваться в коде:\n" +
                f"```\n{'\n'.join(str(x) for x in self.project_dependencies)}\n```\n" +
                code_quality_note + "\nКод, который тебе нужно дополнить:\n" +
                self.initial_code_file)


def parse_homework(blocks):
    task = blocks['html']
    initial_content = blocks['exercise']['exerciseInitialCode'].replace('\n', '')
    code_file_name = get_requested_file_name(initial_content)

    content = bs(task['content'], "html.parser")
    project = ""
    project_link = ""
    for a_tag in content.find_all('a'):
        project_link: str = a_tag['href']
        if project_link.endswith('.zip'):
            project = extract_project_name(project_link)
            break
        a_tag.decompose()

    #TODO: какие-то магические числа, почему именно len(x)>1 ???
    # вообще, надо как-то нормально преобразовывать в текст
    prelude = '\n'.join(x.replace('\n', ' ') for x in content.stripped_strings) # if len(x) > 1
    main_source = get_code_file(project, code_file_name, project_link)
    #
    deps = resolve_all_dependencies(main_source, project)

    page = HomeworkPage(prelude=prelude, initial_code_file=main_source, project_dependencies=deps)
    return page
