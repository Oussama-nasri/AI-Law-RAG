import unittest
from llm.chatbot import Chatbot
from retriever.pdf_pipline import PDFProcessingPipeline
import asyncio


class TestChatbot(unittest.TestCase):
    def test_chatbot(self):
        system_prompt="""
        You are a legal expert assistant. Your task is to respond to legal questions based solely on the provided documents.
        
        Here are some rules to follow:
        
        Only respond to legal questions based on the provided documents.
        
        If you do not know the answer or if the information is not in the documents, clearly state that.
        
        Cite specific sections of the documents to support your answers.
        
        Use clear and precise language, but remain technical when necessary.
        
        Do not make up information that is not present in the documents.
        
        Response format:
        
        Start with a direct answer to the question
        
        Expand with relevant details
        
        Cite specific sources (page numbers, sections)
        
        If necessary, mention the limitations of your response"""

        llm_name = "llama3-70b-8192"

        pdf_path = r"data\pdfs\laws\Analysis-of-decree-law-54-English.pdf"

        pipeline = PDFProcessingPipeline(pdf_path)
        vector_store = pipeline.run()
        chatbot = Chatbot(vector_store=vector_store,system_prompt=system_prompt,llm_name=llm_name)

        query = "Why does the Decree-law's criminalisation of certain offences raise concerns about legal certainty and arbitrary application?"
        #query = "Is it legal to have more than one wife?"
        response = asyncio.run(chatbot.get_response(query))

        print(response)

        self.assertIsInstance(response, dict)


if __name__ == "__main__":
    unittest.main()
