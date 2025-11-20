"""
Test script to verify Qdrant Cloud connection
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()

def test_qdrant_connection():
    """Test connection to Qdrant Cloud"""
    
    print("🔍 Testing Qdrant Cloud Connection...\n")
    
    # Get credentials
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "curriculum_collection")
    
    print(f"📍 URL: {qdrant_url}")
    print(f"🔑 API Key: {qdrant_api_key[:20]}..." if qdrant_api_key else "❌ No API Key")
    print(f"📦 Collection: {collection_name}\n")
    
    try:
        # Initialize client
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
        print("✅ Successfully connected to Qdrant Cloud!\n")
        
        # Get collections
        collections = client.get_collections()
        print(f"📚 Available Collections: {len(collections.collections)}")
        for col in collections.collections:
            print(f"   - {col.name}")
        print()
        
        # Check if our collection exists
        collection_names = [col.name for col in collections.collections]
        
        if collection_name in collection_names:
            print(f"✅ Collection '{collection_name}' exists")
            
            # Get collection info
            collection_info = client.get_collection(collection_name)
            print(f"   📊 Points: {collection_info.points_count}")
            print(f"   📐 Vector Size: {collection_info.config.params.vectors.size}")
            print(f"   📏 Distance: {collection_info.config.params.vectors.distance}")
        else:
            print(f"⚠️  Collection '{collection_name}' does not exist yet")
            print(f"   Creating collection...")
            
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small
                    distance=Distance.COSINE
                ),
            )
            print(f"✅ Collection '{collection_name}' created successfully!")
        
        print("\n✅ All tests passed! Qdrant Cloud is ready to use.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_qdrant_connection()
