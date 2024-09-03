from math import log
from collections import defaultdict


class RelevanceRanker:
    def __init__(self, indexer):
        self.indexer = indexer
        self.idf_cache = {}

    def calculate_tf(self, word, document_id):
        word_positions = self.indexer.get_positions(document_id, word)
        num_terms = len(self.indexer.get_words_in_document(document_id))

        return len(word_positions) / num_terms

    def calculate_idf(self, word):
        if word in self.idf_cache:
            return self.idf_cache[word]

        total_docs = self.indexer.get_total_documents()
        docs_with_word = len(self.indexer.get_ids(word))

        idf_value = log(total_docs / (1 + docs_with_word))
        self.idf_cache[word] = idf_value

        return idf_value

    def rank_documents(self, keywords, document_ids):
        doc_scores = defaultdict(float)

        for word in keywords:
            idf = self.calculate_idf(word)

            for doc_id in document_ids:
                tf = self.calculate_tf(word, doc_id)
                doc_scores[doc_id] += tf * idf

        ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)

        for doc_id, score in ranked_docs:
            yield doc_id
