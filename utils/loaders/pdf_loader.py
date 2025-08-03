from langchain_community.document_loaders import PyPDFLoader

class PDFLoaderService:
  def __init__(self,pdf_path : str):
    self.pdf_path = pdf_path
  
  def load(self):
    loader = PyPDFLoader(self.pdf_path)
    return loader.load()
  