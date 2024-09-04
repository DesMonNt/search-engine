import pytest
from utils import Utils


def test_split_words():
    test_string = "Hello, world! This is a test-string."
    expected_output = ["Hello", "", "world", "", "This", "is", "a", "test", "string", ""]

    result = Utils.split_words(test_string)

    assert result == expected_output


def test_split_words_empty_string():
    test_string = ""
    expected_output = [""]

    result = Utils.split_words(test_string)

    assert result == expected_output


def test_split_words_multiple_splitters():
    test_string = "Hello... world! This is\tanother\ntest."
    expected_output = ["Hello", "", "", "", "world", "", "This", "is", "another", "test", ""]

    result = Utils.split_words(test_string)

    assert result == expected_output


def test_highlight_keywords():
    text = "This is a test string. Test the function!"
    keywords = ["test", "function"]
    expected_output = 'This is a <span class="highlight">test</span> string. <span class="highlight">Test</span> the <span class="highlight">function</span>!'

    result = Utils.highlight_keywords(text, keywords)

    assert result == expected_output


def test_highlight_keywords_case_insensitive():
    text = "Testing the case sensitivity of TEST."
    keywords = ["test"]
    expected_output = 'Testing the case sensitivity of <span class="highlight">TEST</span>.'

    result = Utils.highlight_keywords(text, keywords)

    assert result == expected_output


def test_highlight_keywords_with_quotes():
    text = 'Testing the "quoted" word and \'single-quoted\' word.'
    keywords = ['"quoted"', "'single-quoted'"]
    expected_output = 'Testing the "<span class="highlight">quoted</span>" word and \'single-<span class="highlight">quoted</span>\' word.'

    result = Utils.highlight_keywords(text, keywords)

    assert result == expected_output


def test_highlight_keywords_no_match():
    text = "This is a test string."
    keywords = ["nonexistent"]
    expected_output = "This is a test string."

    result = Utils.highlight_keywords(text, keywords)

    assert result == expected_output
