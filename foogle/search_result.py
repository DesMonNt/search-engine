from os import path


class SearchResult:
    def __init__(self, title: str, snippet: str):
        self.title = path.abspath(title)
        self.snippet = snippet
