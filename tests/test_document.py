import pytest
from document import Document


def test_document_creation():
    doc_id = 1
    title = "Sample Title"
    content = "This is the content of the document."

    document = Document(doc_id, title, content)

    assert document.id == doc_id
    assert document.title == title
    assert document.content == content


def test_document_id_is_int():
    doc_id = 1
    title = "Sample Title"
    content = "This is the content of the document."

    document = Document(doc_id, title, content)

    assert isinstance(document.id, int)


def test_document_title_is_string():
    doc_id = 1
    title = "Sample Title"
    content = "This is the content of the document."

    document = Document(doc_id, title, content)

    assert isinstance(document.title, str)


def test_document_content_is_string():
    doc_id = 1
    title = "Sample Title"
    content = "This is the content of the document."

    document = Document(doc_id, title, content)

    assert isinstance(document.content, str)


def test_document_empty_content():
    doc_id = 2
    title = "Empty Content Document"
    content = ""

    document = Document(doc_id, title, content)

    assert document.id == doc_id
    assert document.title == title
    assert document.content == content
