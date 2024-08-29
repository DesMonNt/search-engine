import os
import logging
from document import Document
from search_result import SearchResult
from search_engine import SearchEngine


class Foogle:
    def __init__(self, root='/.', extensions=os.path.join('configs', 'extensions'), stopwords=os.path.join('configs', 'stopwords')):
        self.documents = dict()
        self.root = root
        self.extensions = Foogle._read_extensions(extensions)
        self.search_engine = SearchEngine(stopwords)
        self._add_files_to_index()

    def search(self, query, rank=False):
        return self._search(query, self.search_engine.search(query, rank=rank))

    def search_or(self, query, rank=False):
        return self._search(query, self.search_engine.search_or(query, rank=rank))

    def _get_snippet(self, query, doc_id, length=200):
        words = query.lower().split()
        positions = []

        for word in words:
            positions.extend(self.search_engine.indexer.get_positions(doc_id, word))

        if not positions:
            return 'Result not found'

        content = self.documents[doc_id].content
        start = max(positions[0] - length // 2, 0)
        end = min(positions[0] + len(query) + length // 2, len(content))
        snippet = content[start:end]

        if end < len(content):
            snippet += "..."

        return snippet

    def _is_valid_extension(self, file_name):
        return any(file_name.endswith(ext) for ext in self.extensions)

    def _search(self, query, docs_ids):
        result = []

        for doc_id in docs_ids:
            if not doc_id in self.documents:
                continue

            if not os.path.exists(os.path.abspath(self.documents[doc_id].title)):
                self.search_engine.remove(doc_id)
                del self.documents[doc_id]
                continue

            result.append(SearchResult(self.documents[doc_id].title, self._get_snippet(query, doc_id)))

        return result

    def _add_files_to_index(self):
        document_id = 1

        for root, dirs, files in os.walk(self.root):
            for file_name in files:

                if not self._is_valid_extension(file_name):
                    continue

                try:
                    path = os.path.join(root, file_name)

                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        document = Document(document_id, path, content)

                        self.search_engine.add_document(document)
                        self.documents[document_id] = document

                        document_id += 1

                except UnicodeDecodeError as e:
                    logging.warning(f"Decode error: {file_name}, error: {e}")

                except PermissionError as e:
                    logging.warning(f"Permission denied: {file_name}, error: {e}")

    @staticmethod
    def _read_extensions(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
