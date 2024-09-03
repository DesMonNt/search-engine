from relevance_ranker import RelevanceRanker
from indexer import Indexer


class SearchEngine:
    def __init__(self, stopwords):
        self.indexer = Indexer(stopwords)
        self.ranker = RelevanceRanker(self.indexer)

    def add_document(self, document):
        self.indexer.add(document)

    def search(self, keywords, rank=False):
        if not keywords:
            return []

        result_docs = set(self.indexer.get_ids(keywords[0]))

        for word in keywords[1:]:
            doc_ids = set(self.indexer.get_ids(word))
            result_docs &= doc_ids

            if not result_docs:
                return []

        result_docs = list(result_docs)

        if rank:
            result_docs = self.ranker.rank_documents(keywords, result_docs)

        return result_docs

    def search_or(self, keywords, rank=False):
        if not keywords:
            return []

        result_docs = set(self.indexer.get_ids(keywords[0]))

        for word in keywords[1:]:
            doc_ids = set(self.indexer.get_ids(word))
            result_docs |= doc_ids

        result_docs = list(result_docs)

        if rank:
            result_docs = self.ranker.rank_documents(keywords, result_docs)

        return result_docs

    def remove(self, doc_id):
        self.indexer.remove(doc_id)
