import os.path

from relevance_ranker import RelevanceRanker
from indexer import Indexer
from os import path


class SearchEngine:
    def __init__(self, stopwords):
        self.indexer = Indexer(stopwords)
        self.ranker = RelevanceRanker(self.indexer)

    def add_document(self, document):
        self.indexer.add(document)

    def search(self, query, rank=False):
        words = query.split()
        result_docs = set()

        for word in words:
            doc_ids = set(self.indexer.get_ids(word))

            if result_docs:
                result_docs &= doc_ids
            else:
                result_docs = doc_ids

        result_docs = list(result_docs)

        if rank:
            result_docs = self.ranker.rank_documents(query, result_docs)

        return result_docs

    def search_or(self, query, rank=False):
        words = query.split()
        result_docs = set()

        for word in words:
            doc_ids = set(self.indexer.get_ids(word))
            result_docs |= doc_ids

        result_docs = list(result_docs)

        if rank:
            result_docs = self.ranker.rank_documents(query, result_docs)

        return result_docs

    def remove(self, doc_id):
        self.indexer.remove(doc_id)