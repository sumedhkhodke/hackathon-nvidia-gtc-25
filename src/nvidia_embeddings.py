"""NVIDIA NeMo Retriever embedding client using direct API calls."""
import os
import requests
from typing import List, Union
from dotenv import load_dotenv
from chromadb import Documents, EmbeddingFunction, Embeddings

load_dotenv()


class NVIDIAEmbeddingClient:
    """Direct API client for NVIDIA embedding models."""
    
    def __init__(self, model: str = "nvidia/nv-embedqa-e5-v5"):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment")
        
        self.model = model
        self.api_url = "https://integrate.api.nvidia.com/v1/embeddings"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def embed_texts(self, texts: Union[str, List[str]], input_type: str = "passage") -> List[List[float]]:
        """Generate embeddings for one or more texts.
        
        Args:
            texts: Single text string or list of text strings to embed
            input_type: Type of input - "passage" for documents, "query" for search queries
            
        Returns:
            List of embedding vectors (each embedding is a list of floats)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        payload = {
            "model": self.model,
            "input": texts,
            "input_type": input_type,  # Required for asymmetric models
            "encoding_format": "float"
        }
        
        response = requests.post(
            self.api_url, 
            headers=self.headers, 
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"NVIDIA API error: {response.status_code} - {response.text}")
        
        result = response.json()
        embeddings = [item["embedding"] for item in result["data"]]
        return embeddings
    
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single query.
        
        Args:
            query: Query text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        return self.embed_texts(query, input_type="query")[0]


class NVIDIAEmbeddingFunction(EmbeddingFunction):
    """ChromaDB-compatible embedding function using NVIDIA API."""
    
    def __init__(self, model: str = "nvidia/nv-embedqa-e5-v5"):
        self.client = NVIDIAEmbeddingClient(model=model)
    
    def __call__(self, input: Documents) -> Embeddings:
        """Generate embeddings for ChromaDB documents.
        
        Args:
            input: List of documents to embed
            
        Returns:
            List of embedding vectors
        """
        return self.client.embed_texts(input, input_type="passage")


# Convenience function for testing
def test_nvidia_embeddings():
    """Test the NVIDIA embedding client."""
    print("🧪 Testing NVIDIA Embedding Client...\n")
    
    try:
        # Initialize client
        client = NVIDIAEmbeddingClient()
        print(f"✅ Client initialized with model: {client.model}")
        
        # Test single text embedding
        test_text = "What is artificial intelligence?"
        embedding = client.embed_query(test_text)
        print(f"\n📝 Test text: '{test_text}'")
        print(f"✅ Embedding generated: {len(embedding)} dimensions")
        print(f"   First 5 values: {embedding[:5]}")
        
        # Test batch embedding
        test_texts = [
            "Sleep quality affects mood",
            "Regular exercise improves energy levels",
            "Work productivity peaks in the morning"
        ]
        embeddings = client.embed_texts(test_texts)
        print(f"\n📚 Batch embedding test:")
        print(f"✅ Generated {len(embeddings)} embeddings")
        for i, text in enumerate(test_texts):
            print(f"   Text {i+1}: '{text}' -> {len(embeddings[i])} dimensions")
        
        # Test ChromaDB function
        embedding_fn = NVIDIAEmbeddingFunction()
        chroma_embeddings = embedding_fn(["Test document for ChromaDB"])
        print(f"\n🔗 ChromaDB embedding function test:")
        print(f"✅ Generated {len(chroma_embeddings)} embedding(s)")
        print(f"   Dimensions: {len(chroma_embeddings[0])}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        raise


if __name__ == "__main__":
    test_nvidia_embeddings()
