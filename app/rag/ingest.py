from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


class RAGIngestor:

    def __init__(self):
        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="payer_rules"
        )

    def ingest_file(self, file_path: str):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        text = path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            raise ValueError(
                "The rule document is empty"
            )

        embedding = self.embedding_model.encode(
            text
        ).tolist()

        self.collection.upsert(
            ids=[path.stem],
            documents=[text],
            embeddings=[embedding],
            metadatas=[
                {
                    "payer": "ABC Health",
                    "source": path.name
                }
            ]
        )

        return {
            "status": "success",
            "file": path.name,
            "collection": "payer_rules"
        }