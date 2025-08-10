import re
import ftfy
from langchain_core.documents import Document
from collections.abc import Iterable

class PDFTextCleaner:
    def __init__(self):
        self.page_number_pattern = re.compile(r"^\s*Page\s+\d+\s*$", re.MULTILINE)
        self.header_patterns = [
            re.compile(r"^Confidential\s*$", re.MULTILINE),
            re.compile(r"^Draft\s*$", re.MULTILINE),
        ]
        self.section_patterns = [
            re.compile(r"Table of Contents", re.IGNORECASE),
            re.compile(r"^References$", re.IGNORECASE | re.MULTILINE),
        ]

    def normalize_text(self, text: str) -> str:
        text = ftfy.fix_text(text)
        return text

    def remove_headers_footers(self, text: str) -> str:
        # Remove page numbers
        text = self.page_number_pattern.sub("", text)
        # Remove custom headers/footers
        for pattern in self.header_patterns:
            text = pattern.sub("", text)
        return text

    def fix_hyphenated_words(self, text: str) -> str:
        # Merge words split across lines with hyphen
        return re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    def merge_broken_lines(self, text: str) -> str:
        # Replace single line breaks within paragraphs with spaces
        return re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    def remove_email(self, text: str) -> str:
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return re.sub(email_pattern, "", text)

    def remove_url(self,text:str) -> str:
        url_pattern = r"https?://\S+|www\.\S+"
        return re.sub(url_pattern, "", text)

    def remove_unwanted_sections(self, text: str) -> str:
        for pattern in self.section_patterns:
            text = pattern.sub("", text)
        return text


    def clean_text(self, text: str) -> str:
        text = self.normalize_text(text)
        text = self.remove_headers_footers(text)
        text = self.fix_hyphenated_words(text)
        text = self.merge_broken_lines(text)
        text = self.remove_unwanted_sections(text)
        text = self.remove_email(text)
        text = self.remove_url(text)

        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def clean_document(self,documents: Iterable[Document]) -> list[Document]:
        cleaned_docs=[]
        for document in documents:

            page_cont = self.clean_text(document.page_content)

            if page_cont :
                new_doc = Document(page_content=page_cont,metadata=document.metadata)
                cleaned_docs.append(new_doc)

        return cleaned_docs



