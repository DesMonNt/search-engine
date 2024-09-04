import pytest
from math import log
from relevance_ranker import RelevanceRanker


@pytest.fixture
def ranker(mocker):
    indexer_mock = mocker.Mock()
    return RelevanceRanker(indexer=indexer_mock)


def test_calculate_tf(ranker, mocker):
    ranker.indexer.get_positions.return_value = [0, 10]
    ranker.indexer.get_words_in_document.return_value = ['test', 'document']

    tf = ranker.calculate_tf('test', 1)

    ranker.indexer.get_positions.assert_called_once_with(1, 'test')
    ranker.indexer.get_words_in_document.assert_called_once_with(1)
    assert tf == 2 / 2


def test_calculate_idf(ranker, mocker):
    ranker.indexer.get_total_documents.return_value = 3
    ranker.indexer.get_ids.return_value = [1, 2, 3]

    idf = ranker.calculate_idf('test')

    ranker.indexer.get_total_documents.assert_called_once()
    ranker.indexer.get_ids.assert_called_once_with('test')
    assert idf == log(3 / 4)


def test_calculate_idf_with_cache(ranker):
    ranker.idf_cache['test'] = 0.5

    idf = ranker.calculate_idf('test')

    assert idf == 0.5


def test_rank_documents(ranker, mocker):
    ranker.indexer.get_total_documents.return_value = 3
    ranker.indexer.get_ids.side_effect = lambda word: [1] if word == 'test' else [2]
    ranker.indexer.get_positions.side_effect = lambda doc_id, word: [0, 10] if doc_id == 1 and word == 'test' else [5]
    ranker.indexer.get_words_in_document.side_effect = lambda doc_id: ['test', 'document'] if doc_id == 1 else ['sample']

    ranked_docs = list(ranker.rank_documents(['test', 'document'], [1, 2]))

    assert ranked_docs == [2, 1]


def test_idf_cache(ranker, mocker):
    ranker.indexer.get_total_documents.return_value = 3
    ranker.indexer.get_ids.return_value = [1]

    _ = ranker.calculate_idf('test')

    assert 'test' in ranker.idf_cache

    cached_idf = ranker.calculate_idf('test')

    assert cached_idf == ranker.idf_cache['test']
