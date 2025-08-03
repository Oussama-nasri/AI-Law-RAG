from langchain_community.vectorstores import Chroma
import os
import shutil

class ChromaVectorStore:
    def __init__(self, persist_directory: str, embedding_model,collection_name):
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        self.vector_store = None
        self._initialize_store()

    def _initialize_store(self):
        """Initialize or load the Chroma vector store."""
        os.makedirs(self.persist_directory, exist_ok=True)
        self.vector_store = Chroma(collection_name=self.collection_name,embedding_function=self.embedding_model,persist_directory=self.persist_directory)
        print(f"Created new Chroma vector store at {self.persist_directory}")

    def add_documents(self, documents):
        """Add documents to the Chroma vector store."""
        if len(self.vector_store.get()["ids"]) == 0:
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
            print(f"Added {len(documents)} new documents to the vector store.")
        else:
            print(f"Documents already exist, skipping addition.")

    def delete_document(self, doc_id: str):
        """Delete a document by its ID."""
        print(f"Deleting document with ID: {doc_id}")
        self.vector_store.persist()  

    def update_document(self, doc_id: str, new_document):
        """Update an existing document."""
        self.delete_document(doc_id)   
        self.add_documents([new_document])  
        print(f"Updated document with ID: {doc_id}")

    def get_similar_documents(self, query: str, top_k=5):
        """Search for documents similar to a query."""
        results = self.vector_store.similarity_search(query=query, k=top_k)
        return results

    def delete_store(self):
        """Delete the entire vector store directory."""
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            print(f"Deleted the Chroma vector store at {self.persist_directory}")
        else:
            print(f"Chroma vector store directory does not exist: {self.persist_directory}")

    def inspect_store(self, show_documents=True, show_metadata=True, show_ids=True, limit=5):
        """Inspect and display the contents of the vector store."""
        if self.vector_store is None:
            print("❌ Vector store is not initialized.")
            return

        data = self.vector_store.get()
        print("--------------",data,"\n---------------")

        total = len(data.get("documents", []))
        print(f"\n📦 Collection '{self.collection_name}' contains {total} document(s):\n")

        for i in range(min(limit, total)):
            print(f"--- Document {i + 1} ---")
            if show_ids:
                print(f"ID: {data['ids'][i]}")
            if show_documents:
                print(f"Content:\n{data['documents'][i]}")
            if show_metadata:
                print(f"Metadata: {data['metadatas'][i]}")
            print()

        if total == 0:
            print("⚠️ No documents found in the store.")

    def return_database_content(self):
        if self.vector_store is None:
            return
        return self.vector_store.get()

    def return_database_collection(self,collection_name:str):
        if self.vector_store is None:
            return
        data = self.vector_store.get()
