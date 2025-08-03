import unittest
from utils.pdf_pipline import PDFProcessingPipeline
from utils.vectorstore.chroma_store import ChromaVectorStore

class TestPDFPipeline(unittest.TestCase):
    def test_pipeline(self):
        pdf_path = r"data\pdfs\laws.pdf"
        db_path = r"data\vectorstore"
        collection_name = "laws_test"
        pipeline = PDFProcessingPipeline(pdf_path,db_path,collection_name)
        vector_store = pipeline.run()
        self.assertIsInstance(vector_store, ChromaVectorStore)

if __name__ == "__main__":
    unittest.main()