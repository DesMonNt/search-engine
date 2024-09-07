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
