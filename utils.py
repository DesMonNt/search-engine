import re
import chardet


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
    def is_text_file(file_path: str) -> bool:
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read(1024)

            encoding = chardet.detect(raw_data)['encoding']
            if not encoding:
                return False

            with open(file_path, 'r', encoding=encoding) as file:
                file.read(1024)

            return True
        except (UnicodeDecodeError, IOError):
            return False
