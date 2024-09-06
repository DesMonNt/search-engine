from document import Document
from utils import Utils


class Indexer:
    def __init__(self, stopwords_path: str | None = None):
        self._words_indexes = dict()
        self._words_in_documents = dict()
        self._stopwords = set()

        if stopwords_path:
            self._load_stopwords(stopwords_path)

    def add(self, document: Document) -> None:
        split_words = Utils.split_words(document.content)

        if document.id not in self._words_in_documents:
            self._words_in_documents[document.id] = []

        word_index = 0
        for word in split_words:
            word = word.lower()
            if len(word) == 0 or word in self._stopwords:
                word_index += len(word) + 1
                continue

            if word not in self._words_indexes:
                self._words_indexes[word] = {}

            if document.id not in self._words_indexes[word]:
                self._words_indexes[word][document.id] = []

            self._words_indexes[word][document.id].append(word_index)
            self._words_in_documents[document.id].append(word)

            word_index += len(word) + 1

    def remove(self, doc_id: int) -> None:
        if doc_id in self._words_in_documents:
            words = self._words_in_documents[doc_id]

            for word in words:
                if doc_id in self._words_indexes[word]:
                    del self._words_indexes[word][doc_id]

            del self._words_in_documents[doc_id]

    def get_ids(self, word: str) -> list[int]:
        return list(self._words_indexes.get(word, {}).keys())

    def get_positions(self, document_id: int, word: str) -> list[int]:
        indexes = self._words_indexes.get(word, {})
        return indexes.get(document_id, [])

    def get_words_in_document(self, document_id: int) -> list[Document]:
        return self._words_in_documents.get(document_id, [])

    def get_total_documents(self) -> int:
        return len(self._words_in_documents)

    def get_all_documents(self) -> set[int]:
        return set(self._words_in_documents.keys())

    def _load_stopwords(self, filepath: str) -> None:
        with open(filepath, 'r') as file:
            for line in file:
                self._stopwords.add(line.strip().lower())
