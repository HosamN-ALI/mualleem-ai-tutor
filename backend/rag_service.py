"""
RAG Service for Mualleem Platform
Handles PDF loading, text chunking, embedding generation, and Qdrant Cloud storage
"""

import os
from typing import List, Optional
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client with Requesty.ai gateway
try:
    requesty_api_key = os.getenv("REQUESTY_API_KEY")
    requesty_base_url = os.getenv("REQUESTY_BASE_URL", "https://router.requesty.ai/v1")
    site_url = os.getenv("SITE_URL", "http://localhost:3000")
    site_name = os.getenv("SITE_NAME", "Mualleem")
    
    if requesty_api_key:
        openai_client = OpenAI(
            api_key=requesty_api_key,
            base_url=requesty_base_url,
            default_headers={
                "HTTP-Referer": site_url,
                "X-Title": site_name
            }
        )
        print(f"✓ Initialized Requesty.ai client with base URL: {requesty_base_url}")
    else:
        openai_client = None
        print("⚠ Warning: REQUESTY_API_KEY not set in .env file")
except Exception as e:
    print(f"✗ Error: Could not initialize Requesty.ai client: {e}")
    openai_client = None

# Qdrant Cloud Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "curriculum_textbooks")

# Text chunking parameters
CHUNK_SIZE = 1000  # characters per chunk
CHUNK_OVERLAP = 200  # overlap between chunks for context continuity


class RAGService:
    """
    Service class for Retrieval-Augmented Generation operations using Qdrant Cloud
    """
    
    def __init__(self):
        """Initialize Qdrant Cloud client and collection"""
        if not QDRANT_URL or not QDRANT_API_KEY:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in .env file")
        
        try:
            self.client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY,
            )
            print(f"✓ Connected to Qdrant Cloud: {QDRANT_URL}")
            
            # Ensure collection exists
            self._ensure_collection_exists()
            
        except Exception as e:
            print(f"✗ Error connecting to Qdrant Cloud: {e}")
            raise
    
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [collection.name for collection in collections]
            
            if COLLECTION_NAME not in collection_names:
                self.client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=3072,  # text-embedding-3-large dimension
                        distance=Distance.COSINE
                    ),
                )
                print(f"✓ Created new collection: {COLLECTION_NAME}")
            else:
                print(f"✓ Using existing collection: {COLLECTION_NAME}")
        except Exception as e:
            print(f"✗ Error ensuring collection exists: {e}")
            raise
    
    def load_pdf(self, pdf_path: str) -> str:
        """
        Load and extract text from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            reader = PdfReader(pdf_path)
            text_content = []
            
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text.strip():
                    text_content.append(text)
                    print(f"✓ Extracted page {page_num}/{len(reader.pages)}")
            
            full_text = "\n\n".join(text_content)
            print(f"✓ Successfully loaded PDF: {len(full_text)} characters")
            return full_text
            
        except Exception as e:
            print(f"✗ Error loading PDF: {str(e)}")
            raise
    
    def split_text_into_chunks(self, text: str, chunk_size: int = CHUNK_SIZE, 
                               overlap: int = CHUNK_OVERLAP) -> List[str]:
        """
        Split text into overlapping chunks for better context preservation
        
        Args:
            text: Input text to split
            chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundaries for Arabic text
            if end < text_length:
                # Look for Arabic sentence endings (. ؟ ! .)
                for delimiter in ['.\n', '؟\n', '!\n', '. ', '؟ ', '! ']:
                    last_delimiter = chunk.rfind(delimiter)
                    if last_delimiter != -1:
                        chunk = text[start:start + last_delimiter + len(delimiter)]
                        break
            
            chunks.append(chunk.strip())
            start += chunk_size - overlap
        
        print(f"✓ Split text into {len(chunks)} chunks")
        return chunks
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI-compatible Requesty.ai gateway.
        
        This function uses the `openai/text-embedding-3-large` model exposed
        via Requesty.ai, and is the single entry point for all embedding
        generation in the RAG service.
        
        Args:
            texts: List of text chunks to embed
            
        Returns:
            List of embedding vectors
        """
        if openai_client is None:
            raise ValueError("Requesty.ai client not initialized. Please set REQUESTY_API_KEY in .env file")
        
        try:
            response = openai_client.embeddings.create(
                model="openai/text-embedding-3-large",  # Requesty format: provider/model
                input=texts,
            )
            
            embeddings = [item.embedding for item in response.data]
            print(f"✓ Generated {len(embeddings)} embeddings via Requesty.ai using openai/text-embedding-3-large")
            return embeddings
            
        except Exception as e:
            print(f"✗ Error generating embeddings: {str(e)}")
            raise
    
    def index_pdf(self, pdf_path: str, document_name: Optional[str] = None) -> dict:
        """
        Complete pipeline: Load PDF, chunk, embed, and store in Qdrant Cloud
        
        Args:
            pdf_path: Path to the PDF file
            document_name: Optional name for the document (defaults to filename)
            
        Returns:
            Dictionary with indexing statistics
        """
        if document_name is None:
            document_name = Path(pdf_path).stem
        
        print(f"\n📚 Starting indexing for: {document_name}")
        
        # Step 1: Load PDF
        text = self.load_pdf(pdf_path)
        
        # Step 2: Split into chunks
        chunks = self.split_text_into_chunks(text)
        
        # Step 3: Generate embeddings (batch processing for efficiency)
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            embeddings = self.generate_embeddings(batch)
            all_embeddings.extend(embeddings)
            print(f"  Processed batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
        
        # Step 4: Store in Qdrant Cloud
        # Get current max ID to avoid conflicts
        try:
            collection_info = self.client.get_collection(COLLECTION_NAME)
            current_count = collection_info.points_count
        except:
            current_count = 0
        
        points = [
            PointStruct(
                id=current_count + i,
                vector=all_embeddings[i],
                payload={
                    "text": chunks[i],
                    "document": document_name,
                    "chunk_index": i,
                    "chunk_size": len(chunks[i])
                }
            )
            for i in range(len(chunks))
        ]
        
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        
        print(f"✓ Successfully indexed {len(chunks)} chunks to Qdrant Cloud\n")
        
        return {
            "document_name": document_name,
            "total_chunks": len(chunks),
            "total_characters": len(text),
            "status": "indexed"
        }
    
    def query_similar_chunks(self, query: str, n_results: int = 5) -> dict:
        """
        Query Qdrant Cloud for similar text chunks based on the question
        
        Args:
            query: User's question
            n_results: Number of similar chunks to retrieve
            
        Returns:
            Dictionary containing relevant context chunks
        """
        try:
            # Generate embedding for the query
            query_embedding = self.generate_embeddings([query])[0]
            
            # Query Qdrant Cloud using query_points API (correct modern API)
            response = self.client.query_points(
                collection_name=COLLECTION_NAME,
                query=query_embedding,
                limit=n_results,
                with_payload=True,
            )
            
            # Format results - query_points returns QueryResponse with points attribute
            context_chunks = []
            for hit in response.points:
                context_chunks.append({
                    "text": hit.payload["text"],
                    "metadata": {
                        "document": hit.payload.get("document", "unknown"),
                        "chunk_index": hit.payload.get("chunk_index", 0),
                        "chunk_size": hit.payload.get("chunk_size", 0)
                    },
                    "score": hit.score
                })
            
            print(f"✓ Retrieved {len(context_chunks)} relevant chunks from Qdrant Cloud")
            
            return {
                "query": query,
                "context_chunks": context_chunks,
                "total_results": len(context_chunks)
            }
            
        except Exception as e:
            print(f"✗ Error querying Qdrant Cloud: {str(e)}")
            return {
                "query": query,
                "context_chunks": [],
                "total_results": 0,
                "error": str(e)
            }
    
    def get_collection_stats(self) -> dict:
        """
        Get statistics about the current collection
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            collection_info = self.client.get_collection(COLLECTION_NAME)
            return {
                "collection_name": COLLECTION_NAME,
                "total_chunks": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size,
                "status": "active",
                "storage": "Qdrant Cloud"
            }
        except Exception as e:
            return {
                "collection_name": COLLECTION_NAME,
                "error": str(e),
                "status": "error"
            }
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            self.client.delete_collection(collection_name=COLLECTION_NAME)
            self._ensure_collection_exists()
            print(f"✓ Cleared collection: {COLLECTION_NAME}")
        except Exception as e:
            print(f"✗ Error clearing collection: {str(e)}")
            raise


# Singleton instance
rag_service = RAGService()


def get_openai_client() -> OpenAI:
    """
    Get the configured OpenAI-compatible client instance used via Requesty.ai.
    
    This client is initialized at module import time using:
      - REQUESTY_API_KEY
      - REQUESTY_BASE_URL (default: https://router.requesty.ai/v1)
    
    It no longer depends on OPENAI_API_KEY directly.
    
    Returns:
        OpenAI client (Requesty.ai gateway)
    """
    return openai_client


# System prompt for the AI tutor
SYSTEM_PROMPT = """أنت معلّم خبير للطلاب العرب. مهمتك هي شرح الإجابات خطوة بخطوة باللغة العربية.

**إرشادات مهمة:**
1. اشرح كل خطوة بوضوح وبساطة
2. استخدم صيغة LaTeX للمعادلات الرياضية (مثال: $x^2 + y^2 = z^2$)
3. كن مشجعاً وإيجابياً في أسلوبك
4. إذا كانت هناك صورة، قم بتحليلها بعناية قبل الإجابة
5. استخدم السياق المقدم من المنهج الدراسي لتقديم إجابات دقيقة
6. إذا لم تكن متأكداً من الإجابة، اذكر ذلك بصراحة

**تنسيق الإجابة:**
- ابدأ بفهم السؤال
- قدم الحل خطوة بخطوة
- اختم بملخص أو نصيحة مفيدة
"""
