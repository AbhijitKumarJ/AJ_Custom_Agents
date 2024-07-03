import os
import hashlib
from typing import List, Tuple
import chromadb
from chromadb.config import Settings
from .document_store import DocumentStore
from ..utils import logger

try:
    import fasttext
    FASTTEXT_AVAILABLE = True
except ImportError:
    FASTTEXT_AVAILABLE = False
    logger.warning("FastText not available. Using fallback embedding method.")

class FastTextChromaStore(DocumentStore):
    def __init__(self, storage_dir: str = "aj_mas/document_storage", model_path: str = "cc.en.300.bin"):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        # Load FastText model if available
        self.model = None
        if FASTTEXT_AVAILABLE and os.path.exists(model_path):
            try:
                self.model = fasttext.load_model(model_path)
                logger.log(f"Loaded FastText model from {model_path}")
            except Exception as e:
                logger.error(f"Error loading FastText model: {str(e)}")
        else:
            logger.warning(f"FastText model not loaded. Using fallback embedding method.")

        # Initialize ChromaDB client
        try:
            self.chroma_client = chromadb.PersistentClient(path=os.path.join(storage_dir, "chroma_db"))
            self.collection = self.chroma_client.get_or_create_collection("documents")
            logger.log(f"Initialized ChromaDB with {len(self.collection.get()['ids'])} documents")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            raise

        self.load_documents()

    def load_documents(self):
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.storage_dir, filename)
                self._process_and_store_document(file_path)

    def _process_and_store_document(self, file_path: str):
        filename = os.path.basename(file_path)
        file_hash = self._get_file_hash(file_path)
        
        existing_docs = self.collection.get(ids=[file_hash])
        if existing_docs["ids"]:
            logger.log(f"Document {filename} already processed and stored.")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            embedding = self._get_document_embedding(content)

            self.collection.add(
                ids=[file_hash],
                embeddings=[embedding],
                metadatas=[{"filename": filename}],
                documents=[content]
            )
            logger.log(f"Processed and stored document: {filename}")
        except Exception as e:
            logger.error(f"Error processing document {filename}: {str(e)}")

    def _get_file_hash(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            return hashlib.md5(file.read()).hexdigest()

    def _get_document_embedding(self, content: str) -> List[float]:
        if self.model:
            words = content.split()
            word_vectors = [self.model.get_word_vector(word) for word in words]
            return list(sum(word_vectors) / len(word_vectors))
        else:
            # Fallback method: use a simple averaging of character codes
            return [sum(ord(c) for c in content) / len(content)] * 300

    def add_document(self, filename: str, content: str):
        file_path = os.path.join(self.storage_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            self._process_and_store_document(file_path)
        except Exception as e:
            logger.error(f"Error adding document {filename}: {str(e)}")

    def retrieve_relevant_content(self, query: str, top_k: int = 3) -> List[Tuple[str, str]]:
        query_embedding = self._get_document_embedding(query)
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            relevant_content = []
            for i in range(len(results["ids"][0])):
                filename = results["metadatas"][0][i]["filename"]
                content = results["documents"][0][i][:500]  # First 500 characters
                relevant_content.append((filename, content))

            logger.log(f"Retrieved {len(relevant_content)} relevant documents for query")
            return relevant_content
        except Exception as e:
            logger.error(f"Error retrieving relevant content: {str(e)}")
            return []