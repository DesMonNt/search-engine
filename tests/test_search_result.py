from os import path

from foogle.search_result import SearchResult


def test_search_result_creation():
    title = "sample_file.txt"
    snippet = "This is a snippet from the document."

    search_result = SearchResult(title, snippet)

    assert search_result.title == path.abspath(title)
    assert search_result.snippet == snippet


def test_search_result_title_is_absolute_path():
    title = "sample_file.txt"
    snippet = "This is a snippet from the document."

    search_result = SearchResult(title, snippet)

    assert path.isabs(search_result.title)
    assert search_result.title == path.abspath(title)


def test_search_result_snippet_is_string():
    title = "sample_file.txt"
    snippet = "This is a snippet from the document."

    search_result = SearchResult(title, snippet)

    assert isinstance(search_result.snippet, str)


def test_search_result_empty_snippet():
    title = "sample_file.txt"
    snippet = ""

    search_result = SearchResult(title, snippet)

    assert search_result.title == path.abspath(title)
    assert search_result.snippet == snippet
