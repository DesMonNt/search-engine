import pytest
from indexer import Indexer
from document import Document


@pytest.fixture
def document():
    return Document(
        document_id=1,
        title="Test Document",
        document_content="This is a test document. This document is just for testing."
    )


@pytest.fixture
def stopwords_file(tmp_path):
    stopwords_file = tmp_path / "stopwords.txt"
    stopwords_file.write_text("is\na\nfor\njust\n")
    return stopwords_file


@pytest.fixture
def indexer_with_stopwords(stopwords_file):
    return Indexer(stopwords=str(stopwords_file))


def test_add_document_without_stopwords(document):
    indexer = Indexer()
    indexer.add(document)

    assert indexer.get_total_documents() == 1
    assert indexer.get_words_in_document(document.id) == [
        'this', 'is', 'a', 'test', 'document', 'this', 'document', 'is', 'just', 'for', 'testing'
    ]
    assert indexer.get_positions(document.id, 'document') == [15, 29]


def test_add_document_with_stopwords(document, indexer_with_stopwords):
    indexer_with_stopwords.add(document)

    assert indexer_with_stopwords.get_total_documents() == 1
    assert indexer_with_stopwords.get_words_in_document(document.id) == [
        'this', 'test', 'document', 'this', 'document', 'testing'
    ]
    assert indexer_with_stopwords.get_positions(document.id, 'document') == [15, 29]


def test_remove_document(document):
    indexer = Indexer()
    indexer.add(document)
    indexer.remove(document.id)

    assert indexer.get_total_documents() == 0
    assert indexer.get_words_in_document(document.id) == []


def test_get_ids(document):
    indexer = Indexer()
    indexer.add(document)

    assert indexer.get_ids('document') == [document.id]
    assert indexer.get_ids('nonexistent') == []


def test_get_positions(document):
    indexer = Indexer()
    indexer.add(document)

    assert indexer.get_positions(document.id, 'this') == [0, 24]
    assert indexer.get_positions(document.id, 'document') == [15, 29]
    assert indexer.get_positions(document.id, 'nonexistent') == []


def test_get_all_documents(document):
    indexer = Indexer()
    indexer.add(document)

    assert indexer.get_all_documents() == {document.id}
