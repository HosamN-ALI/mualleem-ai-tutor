import os
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class RAGEngine:
    def __init__(self):
        # Initialize Requesty.ai client (OpenAI-compatible)
        self.ai_client = OpenAI(
            api_key=os.getenv("REQUESTY_API_KEY"),
            base_url=os.getenv("REQUESTY_BASE_URL"),
            default_headers={
                "HTTP-Referer": os.getenv("SITE_URL", "http://localhost:3000"),
                "X-Title": os.getenv("SITE_NAME", "Mualleem"),
            }
        )
        
        # Initialize Qdrant Cloud client
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "curriculum_collection")
        self.vector_size = 1536  # text-embedding-3-small dimension
        
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        collections = self.qdrant_client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if self.collection_name not in collection_names:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
    
    def load_pdf(self, pdf_path: str) -> str:
        """Load and extract text from PDF"""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """Split text into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        return chunks
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Requesty.ai (OpenAI-compatible)"""
        embeddings = []
        for text in texts:
            response = self.ai_client.embeddings.create(
                model="openai/text-embedding-3-small",
                input=text
            )
            embeddings.append(response.data[0].embedding)
        return embeddings
    
    def index_curriculum(self, pdf_path: str):
        """Index a curriculum PDF into Qdrant Cloud"""
        # Ensure collection exists
        self._ensure_collection_exists()
        
        # Load and chunk PDF
        text = self.load_pdf(pdf_path)
        chunks = self.chunk_text(text)
        
        # Generate embeddings
        embeddings = self.get_embeddings(chunks)
        
        # Prepare points for Qdrant
        points = [
            PointStruct(
                id=i,
                vector=embeddings[i],
                payload={"text": chunks[i], "chunk_id": i}
            )
            for i in range(len(chunks))
        ]
        
        # Upload to Qdrant Cloud
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return len(chunks)
    
    def query_context(self, question: str, n_results: int = 3) -> List[str]:
        """Query Qdrant Cloud for relevant context"""
        # Ensure collection exists
        self._ensure_collection_exists()
        
        # Generate embedding for question
        question_embedding = self.get_embeddings([question])[0]
        
        # Search in Qdrant
        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=question_embedding,
            limit=n_results
        )
        
        # Extract text from results
        contexts = [hit.payload["text"] for hit in search_results]
        return contexts
    
    def generate_answer(self, question: str, context: List[str], image_base64: str = None):
        """Generate answer using Requesty.ai with context"""
        system_prompt = """أنت معلم خبير للطلاب العرب. مهمتك شرح الإجابات خطوة بخطوة باللغة العربية.
استخدم صيغة LaTeX للمعادلات الرياضية (مثال: $x^2$، $$\\frac{a}{b}$$).
كن مشجعاً وواضحاً في شرحك."""

        context_text = "\n\n".join(context) if context else "لا يوجد سياق متاح من المنهج."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"السياق من المنهج:\n{context_text}\n\nالسؤال: {question}"}
        ]
        
        # If image is provided, use vision model
        if image_base64:
            messages[-1]["content"] = [
                {"type": "text", "text": f"السياق من المنهج:\n{context_text}\n\nالسؤال: {question}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]
            model = "openai/gpt-4o"
        else:
            model = "openai/gpt-4o"
        
        response = self.ai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            stream=True
        )
        
        return response
