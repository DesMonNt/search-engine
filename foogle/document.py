class Document:
    def __init__(self, document_id: int, title: str, document_content: str):
        self.id = document_id
        self.title = title
        self.content = document_content
