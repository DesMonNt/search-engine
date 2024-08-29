from math import log
from collections import defaultdict


class RelevanceRanker:
    def __init__(self, indexer):
        self.indexer = indexer

    def calculate_tf(self, word, document_id):
        word_positions = self.indexer.get_positions(document_id, word)

        return len(word_positions) / sum(len(self.indexer.get_positions(document_id, w))
                                         for w in set(self.indexer._words_in_documents[document_id]))

    def calculate_idf(self, word):
        total_docs = len(self.indexer._words_in_documents)
        docs_with_word = len(self.indexer.get_ids(word))

        return log(total_docs / (1 + docs_with_word))

    def rank_documents(self, query, document_ids):
        query_words = query.split()
        doc_scores = defaultdict(float)

        for word in query_words:
            idf = self.calculate_idf(word)

            for doc_id in document_ids:
                tf = self.calculate_tf(word, doc_id)
                doc_scores[doc_id] += tf * idf

        ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)

        for doc_id, score in ranked_docs:
            yield doc_id
