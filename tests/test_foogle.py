import pytest
from foogle import Foogle


@pytest.fixture
def foogle(mocker):
    mock_search_engine = mocker.patch('foogle.SearchEngine', autospec=True)
    mock_search_engine_instance = mock_search_engine.return_value

    mocker.patch('foogle.Document', autospec=True)
    mocker.patch('foogle.SearchResult', autospec=True)

    foogle_instance = Foogle()
    foogle_instance.search_engine = mock_search_engine_instance

    return foogle_instance


def test_read_extensions(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='txt\npdf\n'))

    extensions = Foogle._read_extensions('mock/extensions')

    mock_open.assert_called_once_with('mock/extensions', 'r')
    assert extensions == {'txt', 'pdf'}
