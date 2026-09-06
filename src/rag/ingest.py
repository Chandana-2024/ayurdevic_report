from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


BASE_DIR = Path(__file__).resolve().parent

BOOKS_DIR = BASE_DIR / "books"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"


def load_books():
    documents = []

    for pdf_file in BOOKS_DIR.glob("*.pdf"):
        print(f"Loading: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()

        for doc in docs:
            doc.metadata["source_book"] = pdf_file.name

        documents.extend(docs)

    return documents


def create_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    return chunks


def create_vectorstore(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR)
    )

    return vectorstore


def main():

    print("\n=== AyurGenix RAG Ingestion ===\n")

    documents = load_books()

    print(f"Pages loaded: {len(documents)}")

    chunks = create_chunks(documents)

    create_vectorstore(chunks)

    print("\nRAG vector database created successfully.")


if __name__ == "__main__":
    main()