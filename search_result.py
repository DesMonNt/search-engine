from os import path


class SearchResult:
    def __init__(self, title, snippet):
        self.title = path.abspath(title)
        self.snippet = snippet
