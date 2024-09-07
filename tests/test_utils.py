from charset_normalizer import CharsetMatches

from foogle.utils import Utils


@Utils.keywords_exist
def mock_function(keywords: list[str], some_arg: str) -> list[str]:
    return [f"Keyword: {kw}, Arg: {some_arg}" for kw in keywords]


def test_split_words():
    test_string = "Hello, world! This is a test-string."
    expected_output = ["Hello", "", "world", "", "This", "is", "a", "test", "string", ""]

    result = Utils.split_words(test_string)

    assert result == expected_output


def test_keywords_exist_with_empty_list():
    result = mock_function([], "argument")
    assert result == []


def test_keywords_exist_with_keywords():
    result = mock_function(["test"], "argument")
    assert result == ["Keyword: test, Arg: argument"]


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
    expected_output = ('This is a <span class="highlight">test</span> '
                       'string. <span class="highlight">Test</span> the <span class="highlight">function</span>!')

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
    expected_output = ('Testing the "<span class="highlight">quoted</span>" '
                       'word and \'single-<span class="highlight">quoted</span>\' word.')

    result = Utils.highlight_keywords(text, keywords)

    assert result == expected_output


def test_highlight_keywords_no_match():
    text = "This is a test string."
    keywords = ["nonexistent"]
    expected_output = "This is a test string."

    result = Utils.highlight_keywords(text, keywords)

    assert result == expected_output


def test_is_file_in_folder_valid(mocker):
    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.path.abspath", side_effect=lambda x: x)
    mocker.patch("os.path.commonpath", return_value="/folder")

    assert Utils.is_file_in_folder("/folder/file.txt", "/folder") is True


def test_is_file_in_folder_file_not_exists(mocker):
    mocker.patch("os.path.isfile", return_value=False)
    mocker.patch("os.path.isdir", return_value=True)

    assert Utils.is_file_in_folder("/folder/file.txt", "/folder") is False


def test_is_file_in_folder_folder_not_exists(mocker):
    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("os.path.isdir", return_value=False)

    assert Utils.is_file_in_folder("/folder/file.txt", "/folder") is False


def test_is_file_in_folder_not_in_folder(mocker):
    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.path.abspath", side_effect=lambda x: x)
    mocker.patch("os.path.commonpath", return_value="/other_folder")

    assert Utils.is_file_in_folder("/other_folder/file.txt", "/folder") is False


def test_get_file_encoding_no_result(mocker):
    mocker.patch('charset_normalizer.from_path', return_value=CharsetMatches([]))

    assert Utils.get_file_encoding("fake_path.txt") is None


def test_get_file_encoding_unicode_decode_error(mocker):
    mock_result = mocker.Mock()
    mock_result.encoding = 'utf-8'
    mocker.patch('charset_normalizer.from_path', return_value=CharsetMatches([mock_result]))

    mocker.patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "fake error"))

    assert Utils.get_file_encoding("fake_path.txt") is None


def test_get_file_encoding_io_error(mocker):
    mock_result = mocker.Mock()
    mock_result.encoding = 'utf-8'
    mocker.patch('charset_normalizer.from_path', return_value=CharsetMatches([mock_result]))

    mocker.patch("builtins.open", side_effect=IOError)

    assert Utils.get_file_encoding("fake_path.txt") is None
