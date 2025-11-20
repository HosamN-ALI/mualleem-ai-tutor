# RAG Implementation for Mualleem Platform

## Overview
This document describes the Retrieval-Augmented Generation (RAG) implementation for the Mualleem AI tutoring platform.

## Architecture

### Components

1. **rag_service.py** - Core RAG service with the following features:
   - PDF loading and text extraction
   - Text chunking with overlap for context preservation
   - Embedding generation using OpenAI's `text-embedding-3-small` model
   - Vector storage and retrieval using ChromaDB
   - Semantic search for relevant context

2. **main.py** - FastAPI endpoints integrated with RAG:
   - `POST /upload-curriculum` - Upload and index PDF textbooks
   - `POST /chat` - Chat with AI tutor using RAG context
   - `GET /stats` - Get collection statistics

## How It Works

### 1. PDF Indexing Pipeline

```
PDF Upload → Text Extraction → Text Chunking → Embedding Generation → ChromaDB Storage
```

**Steps:**
1. User uploads a PDF curriculum via `/upload-curriculum`
2. PyPDF extracts text from all pages
3. Text is split into chunks (~1000 characters with 200 character overlap)
4. OpenAI generates embeddings for each chunk
5. Chunks and embeddings are stored in ChromaDB

### 2. Query Pipeline

```
User Question → Query Embedding → Semantic Search → Context Retrieval → AI Response
```

**Steps:**
1. User sends a question (text or image) via `/chat`
2. Question is converted to an embedding
3. ChromaDB finds the 3 most similar chunks
4. Context is added to the system prompt
5. OpenAI GPT-4o generates a step-by-step answer in Arabic

## Configuration

### Environment Variables (.env)

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Server Configuration
PORT=8000
HOST=0.0.0.0
```

### RAG Parameters

```python
CHUNK_SIZE = 1000          # Characters per chunk
CHUNK_OVERLAP = 200        # Overlap between chunks
COLLECTION_NAME = "curriculum_textbooks"
EMBEDDING_MODEL = "text-embedding-3-small"  # Supports Arabic
```

## API Usage

### 1. Upload a Curriculum PDF

```bash
curl -X POST "http://localhost:8000/upload-curriculum" \
  -F "file=@math_textbook.pdf"
```

**Response:**
```json
{
  "message": "تم رفع المنهج وفهرسته بنجاح",
  "filename": "math_textbook.pdf",
  "total_chunks": 150,
  "total_characters": 125000,
  "status": "indexed"
}
```

### 2. Ask a Question (Text Only)

```bash
curl -X POST "http://localhost:8000/chat" \
  -F "question=ما هي قوانين نيوتن للحركة؟"
```

**Response:**
```json
{
  "answer": "قوانين نيوتن للحركة هي...",
  "question": "ما هي قوانين نيوتن للحركة؟",
  "has_image": false,
  "context_used": true,
  "model_used": "gpt-4o-mini"
}
```

### 3. Ask a Question with Image

```bash
curl -X POST "http://localhost:8000/chat" \
  -F "question=حل هذه المسألة الرياضية" \
  -F "image=@problem.jpg"
```

**Response:**
```json
{
  "answer": "**الحل خطوة بخطوة:**\n\n1. نبدأ بتحليل المعادلة...",
  "question": "حل هذه المسألة الرياضية",
  "has_image": true,
  "context_used": true,
  "model_used": "gpt-4o"
}
```

### 4. Get Collection Statistics

```bash
curl "http://localhost:8000/stats"
```

**Response:**
```json
{
  "collection_name": "curriculum_textbooks",
  "total_chunks": 150,
  "status": "active"
}
```

## System Prompt

The AI tutor uses a specialized system prompt in Arabic:

```
أنت معلّم خبير للطلاب العرب. مهمتك هي شرح الإجابات خطوة بخطوة باللغة العربية.

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
```

## Features

### ✅ Implemented

- [x] PDF text extraction using PyPDF
- [x] Intelligent text chunking with overlap
- [x] OpenAI embeddings generation (Arabic support)
- [x] ChromaDB vector storage with persistence
- [x] Semantic search for relevant context
- [x] Text and image question support
- [x] GPT-4o vision integration
- [x] Arabic-first system prompt
- [x] LaTeX math rendering support
- [x] Error handling and validation

### 🔄 Future Enhancements

- [ ] Support for multiple PDF uploads
- [ ] Document management (list, delete PDFs)
- [ ] Streaming responses for real-time feedback
- [ ] Citation of source chunks in answers
- [ ] Multi-language support (English, French)
- [ ] Advanced chunking strategies (semantic splitting)
- [ ] Caching for frequently asked questions
- [ ] Analytics and usage tracking

## Testing

### Run the Test Suite

```bash
cd backend
python3 test_rag.py
```

### Manual Testing

1. **Start the server:**
   ```bash
   cd backend
   python3 -m uvicorn main:app --reload
   ```

2. **Upload a test PDF:**
   - Place a PDF in the `data/` directory
   - Use the `/upload-curriculum` endpoint

3. **Test queries:**
   - Send questions via `/chat` endpoint
   - Try with and without images

## Troubleshooting

### Issue: "OpenAI client not initialized"
**Solution:** Set `OPENAI_API_KEY` in `.env` file

### Issue: "No module named 'chromadb'"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: "No context found for query"
**Solution:** Upload a PDF curriculum first using `/upload-curriculum`

### Issue: ChromaDB persistence errors
**Solution:** Check write permissions for `./chroma_db` directory

## Performance Considerations

- **Embedding Generation:** Batched in groups of 100 for efficiency
- **Vector Search:** ChromaDB uses HNSW algorithm for fast similarity search
- **Chunk Size:** Optimized at 1000 characters for balance between context and precision
- **Model Selection:** 
  - `text-embedding-3-small` for embeddings (cost-effective, Arabic support)
  - `gpt-4o-mini` for text-only questions
  - `gpt-4o` for questions with images

## Dependencies

```
openai==1.12.0           # OpenAI API client
chromadb==0.4.22         # Vector database
pypdf==4.0.1             # PDF text extraction
langchain==0.1.6         # LLM framework utilities
tiktoken==0.5.2          # Token counting
```

## File Structure

```
backend/
├── main.py                    # FastAPI application
├── rag_service.py            # RAG implementation
├── test_rag.py               # Test suite
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── data/                     # PDF storage
│   └── .gitkeep
└── chroma_db/                # ChromaDB persistence (auto-created)
    └── ...
```

## License

Part of the Mualleem AI Tutoring Platform
