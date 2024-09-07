import pytest

from foogle.document import Document
from foogle.foogle import Foogle


@pytest.fixture
def mock_search_engine(mocker):
    return mocker.patch('foogle.foogle.SearchEngine')


@pytest.fixture
def mock_utils(mocker):
    return mocker.patch('foogle.foogle.Utils')


@pytest.fixture
def foogle_instance(mocker):
    search_engine = mocker.Mock()
    search_engine.search_and.return_value = [1]
    search_engine.search_or.return_value = [1, 2]
    search_engine.search_not.return_value = [2]

    foogle = Foogle(stopwords_path='')

    foogle.documents = {
        1: Document(1, 'doc1.txt', 'This is the content of document one.'),
        2: Document(2, 'doc2.txt', 'This is the content of document two.'),
    }
    foogle.search_engine = search_engine

    return foogle


def test_search_and_logic_when_document_is_not_exist(foogle_instance):
    results = foogle_instance.search(['document'], 'and')
    assert len(results) == 0


def test_search_or_logic_when_document_is_not_exist(foogle_instance):
    results = foogle_instance.search(['document'], 'or')
    assert len(results) == 0


def test_search_not_logic_when_document_is_not_exist(foogle_instance):
    results = foogle_instance.search(['document'], 'not')
    assert len(results) == 0


def test_add_files_to_index(mocker, mock_utils, mock_search_engine):
    mocker.patch('builtins.open', mocker.mock_open(read_data='Test document content'))
    mock_utils.get_file_encoding.return_value = 'utf-8'
    mocker.patch('os.walk', return_value=[('test_root', [], ['file1.txt'])])

    foogle = Foogle(root='test_root')
    assert foogle.documents[1].content == 'Test document content'
    mock_search_engine.return_value.add_document.assert_called_once()


def test_get_snippet(foogle_instance, mocker):
    foogle_instance.search_engine.indexer.get_positions = mocker.Mock(return_value=[50])
    foogle_instance.documents[1] = mocker.Mock(
        content="This is the content of a test document. It contains some keywords.")

    snippet = foogle_instance._get_snippet(['test'], 1)

    assert 'test document' in snippet
    assert len(snippet) <= 200
