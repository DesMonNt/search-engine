import logging
import os

from foogle.document import Document
from foogle.search_engine import SearchEngine
from foogle.search_result import SearchResult
from foogle.utils import Utils


class Foogle:
    def __init__(self, root: str = '', encoding: str = 'utf-8',
                 stopwords_path: str = os.path.join('config', 'stopwords')):
        self.documents = dict()
        self.root = root
        self.encoding = encoding
        self.search_engine = SearchEngine(stopwords_path)
        self.disallow_paths, self.disallow_extensions = Utils.read_disallow_index_file(os.path.join(root, 'robots.txt'))
        self._add_files_to_index()

    def search(self, keywords: list[str], logic: str, rank=False) -> list[SearchResult]:
        if logic == 'and':
            return self._search(keywords, self.search_engine.search_and(keywords, rank=rank), logic)
        elif logic == 'or':
            return self._search(keywords, self.search_engine.search_or(keywords, rank=rank), logic)
        return self._search(keywords, self.search_engine.search_not(keywords), logic)

    def _get_snippet(self, keywords: list[str], doc_id: int, length: int = 200) -> str:
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

    def _search(self, keywords: list[str], docs_ids: list[int], logic: str) -> list[SearchResult]:
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

    def _add_files_to_index(self) -> None:
        document_id = 1

        for root, dirs, files in os.walk(self.root):
            rel_path_dir = f'.\\{os.path.relpath(root, self.root).lstrip(".")}'
            if rel_path_dir in self.disallow_paths:
                continue

            for file_name in files:
                path = os.path.join(root, file_name)
                rel_path = os.path.join(rel_path_dir, file_name)
                if rel_path in self.disallow_paths:
                    continue

                extension = os.path.splitext(path)[1]
                if extension in self.disallow_extensions and Utils.is_dir_is_sub_dir_in_set(rel_path,
                                                                                            self.disallow_extensions[
                                                                                                extension]):
                    continue

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
