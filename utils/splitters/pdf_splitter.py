from langchain.text_splitter import RecursiveCharacterTextSplitter


class TextSplitterService:
  def __init__(self,chunk_size = 1000,chunk_overlap=200):
    self.splitter = RecursiveCharacterTextSplitter(
      chunk_size = chunk_size,
      chunk_overlap = chunk_overlap,
      length_function = len
    )
  
  def split(self,documents):
    return self.splitter.split_documents(documents)

