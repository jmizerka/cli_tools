import os
import shutil
import argparse
from typing import List, Optional, Union


def organize_files(folders_paths: List[str], custom_extensions: Optional[List[Union[str, None]]]) -> None:
    for idx, folder_path in enumerate(folders_paths):
        if custom_extensions and custom_extensions[idx] is not None:
            folders = custom_extensions[idx].split()
            categories = {}
            for folder in folders:
                category, extensions = folder.split(':')
                categories[category] = extensions.split(',')
        else:
            categories = {
                'compressed': ['.deb', '.targ.gz', '.zip', '.rar'],
                'texts': ['.txt', '.doc', '.docx', '.odt'],
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
                'audio': ['.mp3', '.wav'],
                'pdfs': ['.pdf'],
                'dbs': ['.csv', '.sql'],
                'spreadsheets': ['.ods', '.xls', '.xlsx', '.xlsm'],
                'executables': ['.bin'],
                'code': ['.py', '.sh', '.html'],
            }

        for category, extension in categories.items():
            os.makedirs(os.path.join(folder_path, category), exist_ok=True)

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                _, extension = os.path.splitext(filename)
                extension = extension.lower()

                for category, extensions in categories.items():
                    if extension in extensions:
                        shutil.move(file_path, os.path.join(folder_path, category))
                        break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage=' clean_folder.py [-h] path1 path2 ... [--custom-extensions "cat1:.ext1,.ext2" cat2:.ext3,.ext4" ...]')
    parser.add_argument('folders_paths', nargs='+', help='paths to folders to clean')
    parser.add_argument('--custom-extensions', nargs='+', help='dir_name:extensions')
    args = parser.parse_args()
    paths: List[str] = args.folders_paths
    extensions: Optional[List[Union[str, None]]] = args.custom_extensions
    if extensions:
        while len(extensions) < len(paths):
            extensions.append(None)
    organize_files(paths, extensions)
