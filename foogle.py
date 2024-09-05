import os
import logging
from document import Document
from search_result import SearchResult
from search_engine import SearchEngine
from utils import Utils


class Foogle:
    def __init__(self, root='', encoding='utf-8', stopwords_path=os.path.join('config', 'stopwords')):
        self.documents = dict()
        self.root = root
        self.encoding = encoding
        self.search_engine = SearchEngine(stopwords_path)
        self._add_files_to_index()

    def search(self, keywords, logic, rank=False):
        if logic == 'and':
            return self._search(keywords, self.search_engine.search_and(keywords, rank=rank), logic)
        elif logic == 'or':
            return self._search(keywords, self.search_engine.search_or(keywords, rank=rank), logic)
        return self._search(keywords, self.search_engine.search_not(keywords), logic)

    def _get_snippet(self, keywords, doc_id, length=200):
        positions = []
        for word in keywords:
            positions.extend(self.search_engine.indexer.get_positions(doc_id, word))

        content = self.documents[doc_id].content
        start = max(positions[0] - length // 2, 0)
        end = min(positions[0] + len(' '.join(keywords)) + length // 2, len(content))
        snippet = content[start:end]

        if start > 0:
            snippet = f'...\n{snippet}'

        if end < len(content):
            snippet = f'{snippet}\n...'

        return snippet

    def _search(self, keywords, docs_ids, logic):
        result = []

        for doc_id in docs_ids:
            if doc_id not in self.documents:
                continue

            if not os.path.exists(os.path.abspath(self.documents[doc_id].title)):
                self.search_engine.remove(doc_id)
                del self.documents[doc_id]
                continue

            if logic == 'not':
                snippet = str()
            else:
                snippet = self._get_snippet(keywords, doc_id)
            result.append(SearchResult(self.documents[doc_id].title, snippet))

        return result

    def _add_files_to_index(self):
        document_id = 1

        for root, dirs, files in os.walk(self.root):
            for file_name in files:
                path = os.path.join(root, file_name)

                if self.encoding == 'auto':
                    file_encoding = Utils.get_file_encoding(path)
                else:
                    file_encoding = self.encoding
                if not file_encoding:
                    continue

                try:
                    with open(path, 'r', encoding=file_encoding) as f:
                        content = f.read()
                        document = Document(document_id, path, content)

                        self.search_engine.add_document(document)
                        self.documents[document_id] = document

                        document_id += 1

                except UnicodeDecodeError as e:
                    logging.warning(f"{file_name}, error: {e}")

                except PermissionError as e:
                    logging.warning(f"{file_name}, error: {e}")
