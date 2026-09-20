import chromadb
from fastembed import TextEmbedding


class PayerRuleIngestor:

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

    def ingest_rule(
        self,
        file_path: str,
        payer_name: str
    ):
        with open(file_path, "r", encoding="utf-8") as file:
            document = file.read()

        embedding = list(
            self.embedding_model.embed([document])
        )[0].tolist()

        self.collection.add(
            documents=[document],
            embeddings=[embedding],
            metadatas=[
                {
                    "payer": payer_name,
                    "source": file_path
                }
            ],
            ids=[payer_name]
        )

        print(
            f"Successfully ingested payer rule: {payer_name}"
        )


if __name__ == "__main__":
    ingestor = PayerRuleIngestor()

    ingestor.ingest_rule(
        "app/rules/payer_rules/abc_health.txt",
        "ABC Health"
    )