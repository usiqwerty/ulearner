import os.path
import re

project_root = "C:\\Users\\Марсианин\\Desktop\\test"


def get_requested_file_name(fixme_string: str):
	res = re.search(r"[\w\W/]*\s+([\w\d]+.cs)\s*[\w\W]*", fixme_string)
	if res and res.group(1):
		return res.group(1)


def get_code_file(filename: str):
	full_path_fn = os.path.join(project_root, filename)
	with open(full_path_fn) as f:
		return f.read()
