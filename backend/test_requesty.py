"""
Test script to verify Requesty.ai integration
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def test_requesty_connection():
    """Test basic connection to Requesty.ai"""
    
    print("🔍 Testing Requesty.ai Configuration...\n")
    
    # Load configuration
    requesty_api_key = os.getenv("REQUESTY_API_KEY")
    requesty_base_url = os.getenv("REQUESTY_BASE_URL", "https://router.requesty.ai/v1")
    site_url = os.getenv("SITE_URL", "http://localhost:3000")
    site_name = os.getenv("SITE_NAME", "Mualleem")
    
    print(f"✓ API Key: {requesty_api_key[:20]}...{requesty_api_key[-10:]}")
    print(f"✓ Base URL: {requesty_base_url}")
    print(f"✓ Site URL: {site_url}")
    print(f"✓ Site Name: {site_name}\n")
    
    if not requesty_api_key:
        print("❌ Error: REQUESTY_API_KEY not found in .env file")
        return False
    
    try:
        # Initialize client
        client = OpenAI(
            api_key=requesty_api_key,
            base_url=requesty_base_url,
            default_headers={
                "HTTP-Referer": site_url,
                "X-Title": site_name
            }
        )
        
        print("📡 Testing Chat Completion (GPT-4o-mini)...")
        
        # Test chat completion
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "user", "content": "قل مرحباً بالعربية"}
            ],
            max_tokens=50
        )
        
        if response.choices:
            answer = response.choices[0].message.content
            print(f"✅ Chat Response: {answer}\n")
        else:
            print("❌ No response choices found\n")
            return False
        
        print("📊 Testing Embeddings (text-embedding-3-small)...")
        
        # Test embeddings
        embedding_response = client.embeddings.create(
            model="openai/text-embedding-3-small",
            input=["مرحباً بك في منصة معلّم"]
        )
        
        if embedding_response.data:
            embedding_dim = len(embedding_response.data[0].embedding)
            print(f"✅ Embedding Generated: {embedding_dim} dimensions\n")
        else:
            print("❌ No embedding data found\n")
            return False
        
        print("🎉 All tests passed! Requesty.ai is configured correctly.\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return False

if __name__ == "__main__":
    success = test_requesty_connection()
    exit(0 if success else 1)
