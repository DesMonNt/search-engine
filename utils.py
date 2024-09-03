import re


class Utils:
    word_splitters = {' ', '.', ',', '!', '?', ':', '-', '\r', '\n', '\t'}
    split_pattern = '|'.join(map(re.escape, word_splitters))

    @staticmethod
    def split_words(string: str) -> list[str]:
        return re.split(Utils.split_pattern, string)

    @staticmethod
    def split_query_using_keywords(keywords: list[str]) -> list[str]:
        # return re.split(r"(?<=\")\s(?=\S)|(?<=\S)\s(?=\")", string)
        result, special_word = [], []
        for word in keywords:
            if word.startswith('"'):
                special_word.append(word)
            elif word.endswith('"'):
                special_word.append(word)
                result.append(' '.join(special_word))
                special_word.clear()
            elif len(special_word) > 0:
                special_word.append(word)
            else:
                result.append(word)
        if len(special_word) > 0:
            result.append(' '.join(special_word))
        return result

    @staticmethod
    def highlight_keywords(text, keywords):
        for word in keywords:
            pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
            text = pattern.sub(f'<span class="highlight">{word}</span>', text)

        return text
