"""
Test script for RAG Service
Run this to verify the RAG implementation works correctly
"""

from rag_service import rag_service, get_openai_client
import os

def test_rag_service():
    """Test the RAG service functionality"""
    
    print("=" * 60)
    print("🧪 Testing RAG Service for Mualleem Platform")
    print("=" * 60)
    
    # Test 1: Check Requesty/OpenAI-compatible client
    print("\n1️⃣ Testing Requesty/OpenAI Client Setup via Requesty.ai...")
    try:
        client = get_openai_client()
        requesty_api_key = os.getenv("REQUESTY_API_KEY")
        requesty_base_url = os.getenv("REQUESTY_BASE_URL", "https://router.requesty.ai/v1")
        if requesty_api_key:
            print("   ✓ Requesty API key configured")
            print(f"   ✓ REQUESTY_API_KEY prefix: {requesty_api_key[:10]}...")
            print(f"   ✓ REQUESTY_BASE_URL: {requesty_base_url}")
        else:
            print("   ⚠️  Warning: REQUESTY_API_KEY not configured in .env file")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test 2: Check ChromaDB collection
    print("\n2️⃣ Testing ChromaDB Collection...")
    try:
        stats = rag_service.get_collection_stats()
        print(f"   ✓ Collection: {stats['collection_name']}")
        print(f"   ✓ Total chunks: {stats['total_chunks']}")
        print(f"   ✓ Status: {stats['status']}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test 3: Test text chunking
    print("\n3️⃣ Testing Text Chunking...")
    try:
        sample_text = "هذا نص تجريبي للاختبار. " * 100
        chunks = rag_service.split_text_into_chunks(sample_text, chunk_size=200, overlap=50)
        print(f"   ✓ Created {len(chunks)} chunks from sample text")
        print(f"   ✓ First chunk length: {len(chunks[0])} characters")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test 4: Check data directory
    print("\n4️⃣ Checking Data Directory...")
    data_dir = "./data"
    if os.path.exists(data_dir):
        pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
        print(f"   ✓ Data directory exists")
        print(f"   ✓ PDF files found: {len(pdf_files)}")
        if pdf_files:
            for pdf in pdf_files:
                print(f"      - {pdf}")
        else:
            print("   ℹ️  No PDF files uploaded yet")
    else:
        print("   ⚠️  Data directory not found")
    
    # Test 5: Test query (if collection has data)
    print("\n5️⃣ Testing Query Functionality...")
    try:
        stats = rag_service.get_collection_stats()
        if stats['total_chunks'] > 0:
            test_query = "ما هي المعادلة الرياضية؟"
            results = rag_service.query_similar_chunks(test_query, n_results=2)
            print(f"   ✓ Query executed successfully")
            print(f"   ✓ Retrieved {results['total_results']} results")
        else:
            print("   ℹ️  No data in collection yet - upload a PDF first")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ RAG Service Test Complete!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("   1. تأكد من ضبط REQUESTY_API_KEY و REQUESTY_BASE_URL في ملف .env")
    print("   2. ارفع ملف PDF للمنهج باستخدام POST /upload-curriculum")
    print("   3. اختبر واجهة الدردشة باستخدام POST /chat")
    print("\n")

if __name__ == "__main__":
    test_rag_service()
