from foogle.document import Document
from foogle.indexer import Indexer
from foogle.relevance_ranker import RelevanceRanker


class SearchEngine:
    def __init__(self, stopwords_path: str):
        self.indexer = Indexer(stopwords_path)
        self.ranker = RelevanceRanker(self.indexer)

    def add_document(self, document: Document) -> None:
        self.indexer.add(document)

    def search_and(self, keywords: list[str], rank: bool = False) -> list[int]:
        if not keywords:
            return []

        result_docs = set(self.indexer.get_ids(keywords[0]))

        for word in keywords[1:]:
            result_docs &= set(self.indexer.get_ids(word))

            if not result_docs:
                return []

        result_docs = list(result_docs)

        if rank:
            result_docs = self.ranker.rank_documents(keywords, result_docs)

        return result_docs

    def search_or(self, keywords: list[str], rank: bool = False) -> list[int]:
        if not keywords:
            return []

        result_docs = set(self.indexer.get_ids(keywords[0]))

        for word in keywords[1:]:
            result_docs |= set(self.indexer.get_ids(word))

        result_docs = list(result_docs)

        if rank:
            result_docs = self.ranker.rank_documents(keywords, result_docs)

        return result_docs

    def search_not(self, keywords: list[str]) -> list[int]:
        if not keywords:
            return []

        result_docs = self.indexer.get_all_documents()

        for word in keywords:
            result_docs -= set(self.indexer.get_ids(word))

        return list(result_docs)

    def remove(self, doc_id: int) -> None:
        self.indexer.remove(doc_id)
