from utils.loaders.pdf_loader import PDFLoaderService
from utils.splitters.pdf_splitter import TextSplitterService
from utils.embeddings.embedding_model import EmbeddingService
from utils.vectorstore.chroma_store import ChromaVectorStore
from utils.text_cleaner.text_cleaner import PDFTextCleaner
import os

class PDFProcessingPipeline:
    def _database_path(self,pdf_path: str):
        try:
            parts = pdf_path.split(os.sep)
            database_name = parts[parts.index("pdfs") + 1]
            root_folder = parts[0]
            database_path = os.path.join(root_folder, database_name)
            return database_path
        except Exception as e:
            print(e)

    def _collection_name(self,pdf_path: str):
        try:
            collection_name = os.path.splitext(os.path.basename(pdf_path))[0]
            return collection_name
        except Exception as e:
            print(e)

    def __init__(self, pdf_path: str):
        self.pdf_path = os.path.normpath(pdf_path)
        self.db_path = self._database_path(self.pdf_path)
        self.collection_name = self._collection_name(self.pdf_path)

    def run(self):
        print(f"Loading PDF: {self.pdf_path}")
        documents = PDFLoaderService(self.pdf_path,"plumber",pages_to_skip=[4]).load()

        documents = PDFTextCleaner().clean_document(documents)
        chunks = TextSplitterService().split(documents)


        embedding_model = EmbeddingService().get_model()


        vector_store = ChromaVectorStore(self.db_path, embedding_model,self.collection_name)

        vector_store.add_documents(chunks)

        return vector_store

