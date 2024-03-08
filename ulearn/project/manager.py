import re
import shutil
import urllib.request
import os
from file_manager.explorer import ulearner_root
def extract_project_name(url: str)-> str:
    r = re.search(r"http[s]?://[\w._/-]+/([\w]+).zip", url)
    return r.group(1)


def download_and_unzip(url: str, force_update = False):
    project_name = extract_project_name(url)
    files = os.listdir(ulearner_root)
    target_fn= f"{project_name}.zip"

    target_full_path = os.path.join(ulearner_root, target_fn)
    if target_fn not in files:
        print(f"Downloading zip: {target_fn}")
        urllib.request.urlretrieve(url, target_full_path)

    out_dir = os.path.join(ulearner_root, project_name)

    if os.path.exists(out_dir):
        if force_update:
            print("Rmdir")
            shutil.rmtree(out_dir)
        else:
            print("Directory exists and not empty")
            return
    print("Unpacking...")
    shutil.unpack_archive(target_full_path, out_dir)
