import os.path
import re

from appconfig import ulearner_root
from ulearn.project.manager import download_and_unzip


def get_requested_file_name(fixme_string: str):
    """
    Достаёт имя файла из поля ввода на странице
    """
    res = re.search(r"[\w\W/]*\s+([\w\d]+.cs)\s*[\w\W]*", fixme_string)
    if res and res.group(1):
        return res.group(1)


def get_code_file(project_name: str, filename: str, url: str):
    """
    :param project_name: Имя проекта
    :param filename: Имя файла с кодом
    :param url: URL файла, на случай, если он не скачан
    :return: Содержимое файла с кодом
    """
    download_and_unzip(url)
    full_path_fn = os.path.join(ulearner_root, project_name, filename)
    try:
        with open(full_path_fn, encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None


excluded_dirs = ['SuspiciousSources']


def recursive_list(directory: str):
    files = []
    for filename in os.listdir(directory):
        entry_path = os.path.join(directory, filename)

        if os.path.isdir(entry_path):
            if filename not in excluded_dirs:
                files += recursive_list(entry_path)
        else:
            if filename.endswith(".cs"):
                files.append(entry_path)
    return files


def list_all_files(project_name: str) -> list[str]:
    """
    Перечислить все .cs файлы проекта
    :param project_name: имя проекта
    :return: Имена файлов
    """

    files = recursive_list(os.path.join(ulearner_root, project_name))
    return files
