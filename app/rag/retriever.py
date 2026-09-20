import chromadb
from sentence_transformers import SentenceTransformer


class RAGRetriever:

    def __init__(self):
        # Load the embedding model only when retrieval is actually needed.
        # This prevents the model from loading during FastAPI startup.
        self.embedding_model = None

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="payer_rules"
        )

    def retrieve(
        self,
        query: str,
        n_results: int = 3
    ) -> list[dict]:

        # Lazy-load the embedding model when RAG is first used.
        if self.embedding_model is None:
            self.embedding_model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        retrieved_rules = []

        for i, document in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i]

            retrieved_rules.append(
                {
                    "document": document,
                    "metadata": metadata
                }
            )

        return retrieved_rules