import os.path
import re

from appconfig import ulearner_root
from ulearn.project.manager import download_and_unzip


def get_requested_file_name(fixme_string: str):
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
    with open(full_path_fn, encoding='utf-8') as f:
        return f.read()


def list_all_files(project_name: str):
    """

    :param project_name:
    :return:
    """
    files = [filename
             for filename in os.listdir(os.path.join(ulearner_root, project_name))
             if filename.endswith(".cs")
             ]
    return files
