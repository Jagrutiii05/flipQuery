from sentence_transformers import SentenceTransformer
import numpy as np
from utils.logger import log
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

class SimpleTextSplitter:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text):
        """Split text into chunks of words with overlap."""
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start = end - self.chunk_overlap if end - self.chunk_overlap > start else end
        return chunks


class Vectorizer:
    def __init__(self):
        # Load SentenceTransformer model locally
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Use our own text splitter instead of langchain
        self.text_splitter = SimpleTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        # Connect to Pinecone to get index dimension
        try:
            self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            self.index_name = os.getenv("PINECONE_INDEX_NAME")
            index_stats = self.pc.describe_index(self.index_name)
            self.target_dim = index_stats.dimension
            log(f"Pinecone index '{self.index_name}' dimension: {self.target_dim}")
        except Exception as e:
            log(f"Error fetching index dimension: {str(e)}", level="ERROR")
            self.target_dim = 384  # default model dimension

    def _pad_vector(self, vec):
        """Pad vector to match Pinecone index dimension."""
        if len(vec) >= self.target_dim:
            return vec
        padding = np.zeros(self.target_dim - len(vec))
        return np.concatenate([vec, padding])

    def create_chunks(self, text):
        """Split text into chunks."""
        try:
            chunks = self.text_splitter.split_text(text)
            log(f"Created {len(chunks)} chunks")
            for chunk in chunks:
                log(chunk)
            return chunks
        except Exception as e:
            log(f"Error creating chunks: {str(e)}", level="ERROR")
            return []

    def create_embeddings(self, chunks):
        """Create embeddings for chunks and pad to index dimension."""
        try:
            embeddings = self.model.encode(
                chunks,
                show_progress_bar=True,
                convert_to_numpy=True
            )
            padded_embeddings = [self._pad_vector(vec).tolist() for vec in embeddings]
            log(f"Created embeddings for {len(padded_embeddings)} chunks (padded to {self.target_dim})")
            return padded_embeddings
        except Exception as e:
            log(f"Error creating embeddings: {str(e)}", level="ERROR")
            return np.array([])

    def create_query_embedding(self, query):
        """Create embedding for query and pad to index dimension."""
        try:
            vec = self.model.encode(query)
            padded_vec = self._pad_vector(vec)
            return padded_vec.tolist()  # Convert numpy array to list
        except Exception as e:
            log(f"Error creating query embedding: {str(e)}", level="ERROR")
            return None
