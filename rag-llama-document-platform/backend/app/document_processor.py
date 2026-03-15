from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def split_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return splitter.split_text(text)

