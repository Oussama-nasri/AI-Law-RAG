from langchain_community.document_loaders import (
    PyPDFLoader,
    PDFPlumberLoader,
)

PDF_LOADER_MAP = {
    "pypdf": PyPDFLoader,
    "plumber": PDFPlumberLoader,
}

class PDFLoaderService:
    def __init__(self, pdf_path: str, loader_type: str = "pypdf", loader_opts: dict = None,pages_to_skip:list = None):
        self.pdf_path = pdf_path
        self.pages_to_skip = pages_to_skip
        loader_opts = loader_opts or {}
        loader_cls = PDF_LOADER_MAP.get(loader_type)

        if not loader_cls:
            raise ValueError(f"Unknown loader type: {loader_type}")

        self.loader = loader_cls(self.pdf_path, **loader_opts)

    def load(self):
        documents= self.loader.load()
        if self.pages_to_skip and documents:
            filtered_docs = [doc for i, doc in enumerate(documents) if i+1 not in self.pages_to_skip]
            return filtered_docs
        else:
            return documents

