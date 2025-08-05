from utils.loaders.pdf_loader import PDFLoaderService
from utils.splitters.pdf_splitter import TextSplitterService
from utils.embeddings.embedding_model import EmbeddingService
from utils.vectorstore.chroma_store import ChromaVectorStore

class PDFProcessingPipeline:
    def __init__(self, pdf_path: str, db_path: str,collection_name):
        self.pdf_path = pdf_path
        self.db_path = db_path
        self.collection_name = collection_name

    def run(self):
        print(f"Loading PDF: {self.pdf_path}")
        documents = PDFLoaderService(self.pdf_path).load()
        print(f"Loaded {len(documents)} pages")

        chunks = TextSplitterService().split(documents)
        print(f"Split into {len(chunks)} chunks")

        embedding_model = EmbeddingService().get_model()
        print("Embedding model initialized")

        vector_store = ChromaVectorStore(self.db_path, embedding_model,self.collection_name)

        vector_store.add_documents(chunks)

        vector_store.show_store()
        return vector_store

