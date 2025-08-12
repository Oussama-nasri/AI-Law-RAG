from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_groq import ChatGroq
from utils.env_loader import EnvLoader



class Chatbot:
    def __init__ (self,vector_store,system_prompt,llm_name):
        self.vector_store = vector_store
        self.system_prompt = system_prompt
        self.llm_name = llm_name
        self.api_key = EnvLoader.load_api_key()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        self.llm = ChatGroq(
            api_key = self.api_key,
            model = self.llm_name,
            temperature=0.2,

        )

        custom_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                self.system_prompt + "\n\nUse the retrieved context to answer the question."),
            HumanMessagePromptTemplate.from_template("Context:\n{context}\n\nQuestion: {question}")
        ])

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k":3}
            ),
            memory = self.memory,
            return_source_documents= True,
            combine_docs_chain_kwargs={"prompt": custom_prompt}

        )

        print("Prompt input vars:", custom_prompt.input_variables)

    async def get_response(self,query):
        result = await self.chain.ainvoke({"question": query})
        sources = []
        for doc in result.get("source_documents", []):
            if hasattr(doc,"metadata") and "source" in doc.metadata:
                sources.append(doc.metadata["source"])
            elif hasattr(doc,"metadata") and "page" in doc.metadata:
                sources.append(doc.metadata["page"])

        response = {
            "answer": result["answer"],
            "sources": list(set(sources))
        }
        return response




