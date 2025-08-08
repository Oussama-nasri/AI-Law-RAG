import unittest
from utils.pdf_pipline import PDFProcessingPipeline
from utils.vectorstore.chroma_store import ChromaVectorStore

class TestPDFPipeline(unittest.TestCase):
    def test_pipeline(self):

        pdf_path = r"data\pdfs\laws\Analysis-of-decree-law-54-English.pdf"
        pipeline = PDFProcessingPipeline(pdf_path)
        vector_store = pipeline.run()

        self.assertIsInstance(vector_store, ChromaVectorStore)

if __name__ == "__main__":
    unittest.main()