import chromadb
from fastembed import TextEmbedding


class RAGRetriever:

    def __init__(self):
        self.embedding_model = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

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

        query_embedding = list(
            self.embedding_model.embed([query])
        )[0].tolist()

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