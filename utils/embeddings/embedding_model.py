from langchain_community.embeddings import HuggingFaceBgeEmbeddings

class EmbeddingService:
  def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", device="cpu"):
    self.model =HuggingFaceBgeEmbeddings(
      model_name = model_name,
      model_kwargs = {"device" : device}
    )
  
  def get_model(self):
    return self.model
  