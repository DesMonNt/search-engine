import re


class Utils:
    @staticmethod
    def highlight_keywords(text, keywords):
        for word in keywords:
            pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
            text = pattern.sub(f'<span class="highlight">{word}</span>', text)

        return text
