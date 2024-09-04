import re
from charset_normalizer import from_path
from os import path


class Utils:
    word_splitters = {' ', '.', ',', '!', '?', ':', '-', '\r', '\n', '\t'}
    split_pattern = '|'.join(map(re.escape, word_splitters))

    @staticmethod
    def split_words(string: str) -> list[str]:
        return re.split(Utils.split_pattern, string)

    @staticmethod
    def highlight_keywords(text, keywords):
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
                file.read(1024)

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
