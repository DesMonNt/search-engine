class Document:
    def __init__(self, document_id, title, document_content):
        self.id = document_id
        self.title = title
        self.content = document_content

    def __str__(self):
        return self.title

    def snippet(self, query, length=200):
        query = query.lower()
        content_lower = self.content.lower()

        start_index = content_lower.find(query)

        if start_index == -1:
            return ""

        start = max(start_index - length // 2, 0)
        end = min(start_index + len(query) + length // 2, len(self.content))

        snippet = self.content[start:end]

        if start > 0:
            snippet = f'...{snippet}'

        if end < len(self.content):
            snippet += "..."

        return snippet
