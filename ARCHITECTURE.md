# 🏗️ Mualleem Platform Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Mualleem AI Tutoring Platform               │
│                         (معلّم - المعلم الذكي)                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│                  │         │                  │         │                  │
│   Frontend       │◄───────►│   Backend        │◄───────►│   Requesty.ai    │
│   (Next.js)      │  HTTP   │   (FastAPI)      │  HTTPS  │   Gateway        │
│                  │         │                  │         │                  │
└──────────────────┘         └──────────────────┘         └──────────────────┘
        │                            │                             │
        │                            │                             │
        ▼                            ▼                             ▼
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│  User Interface  │         │   ChromaDB       │         │  OpenAI Models   │
│  - Chat UI       │         │   (Vector DB)    │         │  - GPT-4o        │
│  - Image Upload  │         │   - Embeddings   │         │  - GPT-4o-mini   │
│  - RTL Support   │         │   - RAG Context  │         │  - Embeddings    │
│  - LaTeX Render  │         │                  │         │                  │
└──────────────────┘         └──────────────────┘         └──────────────────┘
```

## Data Flow

### 1. Text Question Flow
```
Student Question (Arabic)
        │
        ▼
┌─────────────────────────────┐
│  Frontend (Next.js)         │
│  - Validate input           │
│  - Show loading state       │
└─────────────────────────────┘
        │
        ▼ POST /chat
┌─────────────────────────────┐
│  Backend (FastAPI)          │
│  1. Query ChromaDB for      │
│     relevant context        │
│  2. Build prompt with       │
│     context + question      │
└─────────────────────────────┘
        │
        ▼ API Request
┌─────────────────────────────┐
│  Requesty.ai Gateway        │
│  - Route to OpenAI          │
│  - Model: gpt-4o-mini       │
│  - Cache optimization       │
└─────────────────────────────┘
        │
        ▼ Response
┌─────────────────────────────┐
│  Backend Processing         │
│  - Format response          │
│  - Add metadata             │
└─────────────────────────────┘
        │
        ▼ JSON Response
┌─────────────────────────────┐
│  Frontend Display           │
│  - Render Arabic text       │
│  - Parse LaTeX equations    │
│  - Show step-by-step        │
└─────────────────────────────┘
```

### 2. Image Question Flow
```
Student uploads image + question
        │
        ▼
┌─────────────────────────────┐
│  Frontend                   │
│  - Preview image            │
│  - Validate file type       │
└─────────────────────────────┘
        │
        ▼ POST /chat (multipart)
┌─────────────────────────────┐
│  Backend                    │
│  1. Save image temporarily  │
│  2. Convert to base64       │
│  3. Query ChromaDB          │
│  4. Build vision prompt     │
└─────────────────────────────┘
        │
        ▼ Vision API Request
┌─────────────────────────────┐
│  Requesty.ai → OpenAI       │
│  - Model: gpt-4o (vision)   │
│  - Image + text analysis    │
└─────────────────────────────┘
        │
        ▼ Response
┌─────────────────────────────┐
│  Frontend Display           │
│  - Show image               │
│  - Render solution          │
│  - LaTeX equations          │
└─────────────────────────────┘
```

### 3. PDF Curriculum Indexing Flow
```
Admin uploads PDF textbook
        │
        ▼
┌─────────────────────────────┐
│  POST /upload-curriculum    │
│  - Validate PDF             │
│  - Save to ./data/          │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  RAG Service                │
│  1. Extract text (PyPDF)    │
│  2. Split into chunks       │
│     (~1000 chars each)      │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  Generate Embeddings        │
│  - Via Requesty.ai          │
│  - Model: text-embedding-   │
│    3-small                  │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  Store in ChromaDB          │
│  - Vector embeddings        │
│  - Original text chunks     │
│  - Metadata (doc, index)    │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  Ready for RAG Queries      │
│  ✓ Indexed and searchable   │
└─────────────────────────────┘
```

## Component Details

### Frontend (Next.js 14+)
- **Framework**: Next.js with App Router
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Math Rendering**: react-katex / react-latex-next
- **Language**: Arabic (RTL support)
- **Features**:
  - Real-time chat interface
  - Image upload and preview
  - LaTeX equation rendering
  - Responsive design

### Backend (FastAPI)
- **Framework**: FastAPI (Python 3.11+)
- **Server**: Uvicorn
- **Features**:
  - RESTful API endpoints
  - File upload handling
  - CORS middleware
  - Error handling
  - Async operations

### RAG System
- **Vector DB**: ChromaDB (local persistence)
- **PDF Processing**: PyPDF
- **Chunking**: 1000 chars with 200 char overlap
- **Embeddings**: OpenAI text-embedding-3-small
- **Query**: Semantic similarity search

### AI Provider (Requesty.ai)
- **Gateway**: https://router.requesty.ai/v1
- **Models Used**:
  - `openai/gpt-4o` - Vision + text (for images)
  - `openai/gpt-4o-mini` - Text only (faster, cheaper)
  - `openai/text-embedding-3-small` - Embeddings
- **Features**:
  - Unified API for 300+ models
  - Automatic caching
  - Cost optimization
  - Usage tracking
  - Failover support

## API Endpoints

### Health & Status
```
GET  /              - Welcome message
GET  /health        - Health check
GET  /stats         - Collection statistics
```

### Core Features
```
POST /upload-curriculum  - Upload and index PDF textbook
POST /chat              - Ask question (text + optional image)
```

## Environment Variables

```env
# Requesty.ai Configuration
REQUESTY_API_KEY=rqsty-sk-...
REQUESTY_BASE_URL=https://router.requesty.ai/v1

# Site Information
SITE_URL=http://localhost:3000
SITE_NAME=Mualleem - AI Tutoring Platform

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Server
PORT=8000
HOST=0.0.0.0
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14+ | React framework with SSR |
| Styling | Tailwind CSS | Utility-first CSS |
| Math | react-katex | LaTeX rendering |
| Backend | FastAPI | Python web framework |
| Server | Uvicorn | ASGI server |
| Vector DB | ChromaDB | Embeddings storage |
| PDF | PyPDF | Text extraction |
| AI Gateway | Requesty.ai | Unified AI access |
| LLM | GPT-4o / GPT-4o-mini | Text generation |
| Vision | GPT-4o | Image analysis |
| Embeddings | text-embedding-3-small | Vector generation |

## Security Considerations

1. **API Keys**: Stored in `.env` (not committed)
2. **CORS**: Configured for localhost:3000
3. **File Upload**: Validated file types (PDF, images)
4. **HTTPS**: All external API calls use HTTPS
5. **Temp Files**: Cleaned up after processing

## Performance Optimizations

1. **Model Selection**: Auto-select cheaper model for text-only
2. **Caching**: Requesty.ai built-in caching
3. **Batch Processing**: Embeddings generated in batches
4. **Async Operations**: FastAPI async endpoints
5. **Vector Search**: ChromaDB optimized similarity search

## Scalability Considerations

### Current Setup (MVP)
- Local ChromaDB persistence
- Single server instance
- File-based storage

### Future Enhancements
- Cloud-hosted ChromaDB (e.g., Chroma Cloud)
- Distributed backend (load balancing)
- Object storage for PDFs (S3, GCS)
- Redis caching layer
- WebSocket for real-time streaming
- Multi-tenant support

## Monitoring & Observability

1. **Requesty.ai Dashboard**: API usage, costs, performance
2. **FastAPI Logs**: Request/response logging
3. **ChromaDB Stats**: Collection size, query performance
4. **Error Tracking**: Exception handling and logging

---

**Architecture Version**: 1.0  
**Last Updated**: November 20, 2025  
**Status**: Production Ready
