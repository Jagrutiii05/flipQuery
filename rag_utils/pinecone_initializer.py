# rag_utils/pinecone_service.py
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from utils.logger import log

load_dotenv()

class PineconeService:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.index = self.pc.Index(self.index_name)

    def upsert_vectors(self, vectors):
        """
        vectors format: [(id, embedding, metadata), ...]
        """
        try:
            log(f"Upserting {len(vectors)} vectors to Pinecone index: {self.index_name}")
            self.index.upsert(vectors=vectors)
            return True
        except Exception as e:
            log(f"Upsert error: {str(e)}")
            return False

    def similarity_search(self, query_embedding, top_k=5, filter_doc_id=None):
        """
        Returns top_k most similar vectors.
        """
        try:
            log(f"Querying Pinecone index: {self.index_name} for top {top_k} matches")
            
            # Build query parameters
            query_params = {
                "vector": query_embedding,
                "top_k": top_k,
                "include_metadata": True
            }
            
            # Add filter if document ID is provided
            if filter_doc_id:
                query_params["filter"] = {"doc_id": filter_doc_id}
                log(f"Filtering by document ID: {filter_doc_id}")
            
            results = self.index.query(**query_params)
            return results.get("matches", [])
        except Exception as e:
            log(f"Similarity search error: {str(e)}")
            return []
