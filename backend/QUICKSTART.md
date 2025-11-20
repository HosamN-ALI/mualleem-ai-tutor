# Quick Start Guide - Mualleem RAG Backend

## Prerequisites

- Python 3.9+
- OpenAI API Key

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Edit the `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Test the RAG Service

```bash
python3 test_rag.py
```

Expected output:
```
✓ Created new collection: curriculum_textbooks
✓ OpenAI client initialized successfully
✓ Collection: curriculum_textbooks
✓ Total chunks: 0
✓ Status: active
```

### 4. Start the Server

```bash
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:

```bash
python3 main.py
```

The server will start at: `http://localhost:8000`

### 5. Test the API

#### Check Health
```bash
curl http://localhost:8000/health
```

#### Upload a PDF Curriculum
```bash
curl -X POST "http://localhost:8000/upload-curriculum" \
  -F "file=@/path/to/your/textbook.pdf"
```

#### Ask a Question
```bash
curl -X POST "http://localhost:8000/chat" \
  -F "question=ما هي قوانين نيوتن للحركة؟"
```

#### Ask with Image
```bash
curl -X POST "http://localhost:8000/chat" \
  -F "question=حل هذه المسألة" \
  -F "image=@/path/to/problem.jpg"
```

#### Get Statistics
```bash
curl http://localhost:8000/stats
```

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Directory Structure

```
backend/
├── main.py              # FastAPI application with endpoints
├── rag_service.py       # RAG implementation (PDF, embeddings, ChromaDB)
├── test_rag.py          # Test suite
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (add your API key here)
├── data/                # PDF storage directory
└── chroma_db/           # ChromaDB vector database (auto-created)
```

## Key Features

✅ **PDF Processing:** Automatically extracts and chunks text from uploaded PDFs  
✅ **Semantic Search:** Uses OpenAI embeddings for intelligent context retrieval  
✅ **Vision Support:** Handles both text and image-based questions  
✅ **Arabic-First:** Optimized for Arabic language tutoring  
✅ **LaTeX Math:** Supports mathematical notation in responses  
✅ **Persistent Storage:** ChromaDB saves indexed content locally  

## Troubleshooting

### "OpenAI client not initialized"
- Make sure `OPENAI_API_KEY` is set in `.env`
- Restart the server after updating `.env`

### "No module named 'chromadb'"
- Run: `pip install -r requirements.txt`

### Port 8000 already in use
- Change port: `uvicorn main:app --port 8001`
- Or kill existing process: `lsof -ti:8000 | xargs kill`

### ChromaDB errors
- Delete `chroma_db/` directory and restart
- Check write permissions

## Next Steps

1. **Upload a curriculum PDF** to enable RAG functionality
2. **Test with sample questions** to verify responses
3. **Integrate with frontend** (Next.js app in `../frontend/`)
4. **Monitor usage** via `/stats` endpoint

## Support

For detailed implementation details, see: `RAG_IMPLEMENTATION.md`

---

**Mualleem Platform** - AI-Powered Tutoring for Arab Students 🎓
