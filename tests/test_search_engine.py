import pytest

from foogle.document import Document
from foogle.search_engine import SearchEngine


@pytest.fixture
def search_engine(mocker):
    mocker.patch('foogle.search_engine.Indexer')
    mocker.patch('foogle.search_engine.RelevanceRanker')

    engine = SearchEngine(stopwords_path="stopwords")
    return engine


def test_add_document(search_engine):
    doc = Document(document_id=1, title="Test Document", document_content="Test content")

    search_engine.add_document(doc)

    search_engine.indexer.add.assert_called_once_with(doc)


def test_search_and(search_engine):
    search_engine.indexer.get_ids.side_effect = lambda word: [1] if word == "test" else [1, 2]

    result = search_engine.search_and(["test", "document"])

    search_engine.indexer.get_ids.assert_any_call("test")
    search_engine.indexer.get_ids.assert_any_call("document")
    assert result == [1]


def test_search_and_no_results(search_engine):
    search_engine.indexer.get_ids.side_effect = lambda word: []

    result = search_engine.search_and(["nonexistent"])

    search_engine.indexer.get_ids.assert_called_once_with("nonexistent")
    assert result == []


def test_search_or(search_engine):
    search_engine.indexer.get_ids.side_effect = lambda word: [1] if word == "test" else [2]

    result = search_engine.search_or(["test", "document"])

    search_engine.indexer.get_ids.assert_any_call("test")
    search_engine.indexer.get_ids.assert_any_call("document")
    assert sorted(result) == [1, 2]


def test_search_or_no_results(search_engine):
    search_engine.indexer.get_ids.side_effect = lambda word: []

    result = search_engine.search_or(["nonexistent"])

    search_engine.indexer.get_ids.assert_called_once_with("nonexistent")
    assert result == []


def test_search_not(search_engine):
    search_engine.indexer.get_all_documents.return_value = {1, 2, 3}
    search_engine.indexer.get_ids.return_value = [1]

    result = search_engine.search_not(["test"])

    search_engine.indexer.get_all_documents.assert_called_once()
    search_engine.indexer.get_ids.assert_called_once_with("test")
    assert sorted(result) == [2, 3]


def test_search_and_with_ranking(search_engine):
    search_engine.indexer.get_ids.side_effect = lambda word: [1] if word == "test" else [1, 2]
    search_engine.ranker.rank_documents.return_value = [2, 1]

    result = search_engine.search_and(["test", "document"], rank=True)

    search_engine.indexer.get_ids.assert_any_call("test")
    search_engine.indexer.get_ids.assert_any_call("document")
    search_engine.ranker.rank_documents.assert_called_once_with(["test", "document"], [1])
    assert result == [2, 1]


def test_remove_document(search_engine):
    doc_id = 1

    search_engine.remove(doc_id)

    search_engine.indexer.remove.assert_called_once_with(doc_id)
