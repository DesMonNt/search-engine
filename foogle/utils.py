import re
from os import path
from string import punctuation, whitespace

from charset_normalizer import from_path


class Utils:
    split_pattern = '|'.join(map(re.escape, list(punctuation + whitespace)))

    @staticmethod
    def split_words(string: str) -> list[str]:
        return re.split(Utils.split_pattern, string)

    @staticmethod
    def keywords_exist(method):
        def wrapper(keywords: list[str], *args, **kwargs):
            if not keywords:
                return []
            return method(keywords, *args, **kwargs)

        return wrapper

    @staticmethod
    def highlight_keywords(text: str, keywords: list[str]) -> str:
        for word in keywords:
            word = word.strip('"').strip("'")
            pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
            text = pattern.sub(lambda match: f'<span class="highlight">{match.group(0)}</span>', text)

        return text

    @staticmethod
    def get_file_encoding(file_path: str) -> str | None:
        try:
            result = from_path(file_path).best()
            if not result:
                return

            encoding = result.encoding
            with open(file_path, 'r', encoding=encoding) as file:
                file.read(128)

            return encoding
        except (UnicodeDecodeError, IOError):
            return

    @staticmethod
    def is_file_in_folder(file_path: str, folder_path: str) -> bool:
        file_path = path.abspath(file_path)
        folder_path = path.abspath(folder_path)

        if not path.isfile(file_path) or not path.isdir(folder_path):
            return False

        return path.commonpath([file_path, folder_path]) == folder_path

    @staticmethod
    def read_disallow_index_file(filepath: str) -> (set[str], dict[str]):
        if not path.isfile(filepath):
            return set(), dict()
        paths, file_extensions = {f".\\{path.basename(filepath)}"}, dict()
        for line in map(
                lambda x: ''.join(('.\\', x.strip('.').strip('/').strip('\\').replace('/', '\\'))),
                open(filepath, encoding=Utils.get_file_encoding(filepath)).read().splitlines()
        ):
            if '*' in line:
                dir_path, file_extension = path.splitext(line)
                dir_path = dir_path.rstrip('\\*')
                if file_extension not in file_extensions:
                    file_extensions[file_extension] = {dir_path}
                else:
                    file_extensions[file_extension].add(dir_path)
            else:
                paths.add(line)
        return paths, file_extensions

    @staticmethod
    def is_dir_is_sub_dir_in_set(dir_path: str, dir_paths_check: set[str]) -> bool:
        for folder in dir_paths_check:
            if dir_path.startswith(folder):
                return True
        return False
