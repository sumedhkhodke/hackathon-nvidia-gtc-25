"""Vector database operations for personal lifelog data."""
import pandas as pd
import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os
from src.nvidia_embeddings import NVIDIAEmbeddingFunction


class LifelogDataStore:
    """Manages storage and retrieval of personal lifelog data using ChromaDB with NVIDIA embeddings."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize the vector database with NVIDIA embedding function.
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_directory = persist_directory
        self.embedding_function = NVIDIAEmbeddingFunction()
        
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        self.collection_name = "lifelog_entries"
        self.collection = None
        
    def load_and_store_csv(self, csv_path: str) -> int:
        """Load CSV data and store in vector database.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            Number of entries stored
        """
        # Load CSV
        df = pd.read_csv(csv_path)
        
        # Create or get collection with NVIDIA embedding function
        try:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Personal lifelog with NVIDIA embeddings"}
            )
        except Exception:
            self.collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
        
        # Prepare data for embedding
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in df.iterrows():
            # Create a rich text representation
            doc_text = f"Date: {row['date']}\nCategory: {row['category']}\nEntry: {row['entry']}\nMood Score: {row['mood_score']}"
            documents.append(doc_text)
            
            metadatas.append({
                "date": str(row['date']),
                "category": str(row['category']),
                "mood_score": str(row['mood_score'])
            })
            
            ids.append(f"entry_{idx}")
        
        # Add to collection (ChromaDB will use NVIDIA embeddings)
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(documents)
    
    def query(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """Query the vector database for relevant entries.
        
        Args:
            query_text: Natural language query
            n_results: Number of results to return
            
        Returns:
            List of relevant entries with metadata
        """
        if not self.collection:
            self.collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                })
        
        return formatted_results
    
    def get_stats(self) -> Dict:
        """Get statistics about the stored data.
        
        Returns:
            Dictionary with database statistics
        """
        if not self.collection:
            try:
                self.collection = self.client.get_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_function
                )
            except Exception:
                return {"total_entries": 0, "status": "No data loaded"}
        
        count = self.collection.count()
        return {
            "total_entries": count,
            "collection_name": self.collection_name,
            "status": "Ready"
        }


# Convenience function for quick testing
def test_datastore():
    """Test the datastore with sample data."""
    store = LifelogDataStore()
    
    # Load sample data
    count = store.load_and_store_csv("data/sample_lifelog.csv")
    print(f"✅ Loaded {count} entries into vector database")
    
    # Test query
    results = store.query("sleep quality patterns", n_results=3)
    print(f"\n🔍 Query: 'sleep quality patterns'")
    print(f"Found {len(results)} relevant entries:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['content'][:100]}...")
    
    # Stats
    stats = store.get_stats()
    print(f"\n📊 Database Stats: {stats}")


if __name__ == "__main__":
    test_datastore()

