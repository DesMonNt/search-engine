import re


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
