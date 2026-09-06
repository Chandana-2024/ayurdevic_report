from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


class AyurvedaRetriever:

    def __init__(self):

        project_root = Path(__file__).resolve().parents[2]

        # IMPORTANT:
        # This is the Chroma database created during ingestion.
        chroma_path = project_root / "src" / "rag" / "vectorstore"

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = Chroma(
            persist_directory=str(chroma_path),
            embedding_function=embeddings,
        )

    def search(self, query: str, k: int = 5):

        results = self.vector_store.similarity_search(
            query,
            k=k
        )

        return results


if __name__ == "__main__":

    retriever = AyurvedaRetriever()

    query = "Agni digestive fire Mandagni Vishamagni Samagni Tikshnagni"

    results = retriever.search(query, k=5)

    print("\n======================================")
    print("AYURGENIX RAG RETRIEVER TEST")
    print("======================================")

    print(f"\nQuery: {query}\n")

    if not results:
        print("❌ No results found.")
    else:

        for i, result in enumerate(results, start=1):

            print(f"\n--- Result {i} ---")

            print(result.page_content[:1500])

            print("\nSource Information:")

            metadata = result.metadata

            print(
                "Book:",
                metadata.get("source_book", "Unknown")
            )

            print(
                "Page:",
                metadata.get("page", "Unknown")
            )

            print(
                "Author:",
                metadata.get("author", "Unknown")
            )

            print()