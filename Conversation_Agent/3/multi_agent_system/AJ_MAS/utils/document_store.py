import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .logger import logger


class DocumentStore:
    def __init__(self, storage_dir="AJ_MAS/document_storage"):
        self.storage_dir = storage_dir
        self.documents = {}
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None

        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        self.load_documents()

    def load_documents(self):
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.storage_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.documents[filename] = content

        if self.documents:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.documents.values())

        logger.log(f"Loaded {len(self.documents)} documents")

    def add_document(self, filename, content):
        file_path = os.path.join(self.storage_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        self.documents[filename] = content
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents.values())
        logger.log(f"Added new document: {filename}")

    def retrieve_relevant_content(self, query, top_k=3):
        if not self.documents:
            return []

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]

        relevant_content = []
        for idx in top_indices:
            filename = list(self.documents.keys())[idx]
            content = self.documents[filename]
            relevant_content.append(
                (filename, content[:500])
            )  # Return first 500 characters

        logger.log(f"Retrieved {len(relevant_content)} relevant documents for query")
        return relevant_content


document_store = DocumentStore()
