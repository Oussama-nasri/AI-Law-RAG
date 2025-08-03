import unittest
from utils.loaders.pdf_loader import PDFLoaderService

class TestPDFLoader(unittest.TestCase):
  def test_load_pdf(self):
    pdf_path = r"data\pdfs\laws.pdf"
    loader = PDFLoaderService(pdf_path)
    documents = loader.load()
    self.assertIsInstance(documents, list)
    self.assertGreater(len(documents), 0, "PDF should have pages")
    

if __name__ == "__main__":
    unittest.main()