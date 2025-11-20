# 🚀 Quick Start Guide - Mualleem Platform

## Current Status

✅ **Backend**: Implemented (FastAPI + RAG + OpenAI)  
✅ **Frontend**: Implemented (Next.js + React + LaTeX)  
✅ **Development Server**: Running on http://localhost:3000

---

## 🏃 Running the Application

### 1. Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```
**Backend URL**: http://localhost:8000

### 2. Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
**Frontend URL**: http://localhost:3000

---

## 📋 Testing the Application

### Step 1: Upload Curriculum (One-time setup)
```bash
# Place your PDF textbook in backend/data/
cp your_textbook.pdf backend/data/curriculum.pdf

# Upload and index it
curl -X POST http://localhost:8000/upload-curriculum \
  -F "file=@backend/data/curriculum.pdf"
```

### Step 2: Test Chat Interface
1. Open http://localhost:3000 in your browser
2. Type a question in Arabic: **"ما هو قانون فيثاغورس؟"**
3. Or upload an image of a math problem
4. Click **"إرسال"** (Send)
5. View the AI response with LaTeX equations

---

## 🧪 API Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Chat Endpoint (Text Only)
```bash
curl -X POST http://localhost:8000/chat \
  -F "question=ما هو قانون فيثاغورس؟"
```

### Chat Endpoint (With Image)
```bash
curl -X POST http://localhost:8000/chat \
  -F "question=حل هذه المسألة" \
  -F "image=@path/to/math_problem.jpg"
```

---

## 📁 Project Structure

```
/vercel/sandbox/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── rag_service.py       # RAG logic
│   ├── rag_engine.py        # ChromaDB integration
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # OpenAI API key
│   └── data/                # PDF storage
│
└── frontend/
    ├── app/
    │   ├── layout.tsx       # RTL layout
    │   ├── page.tsx         # Home page
    │   └── globals.css      # Styles
    ├── components/
    │   ├── ChatInterface.tsx  # Main chat UI
    │   └── ChatBubble.tsx     # Message display
    └── package.json
```

---

## 🔑 Environment Setup

### Backend `.env` file
```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Get your API key**: https://platform.openai.com/api-keys

---

## 🎯 Key Features

| Feature | Status | Description |
|---------|--------|-------------|
| Text Chat | ✅ | Ask questions in Arabic |
| Image Upload | ✅ | Upload math problem images |
| LaTeX Rendering | ✅ | Display equations beautifully |
| RAG Integration | ✅ | Context from PDF curriculum |
| RTL Support | ✅ | Proper Arabic text direction |
| Vision AI | ✅ | GPT-4o analyzes images |

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9

# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Check if port 3000 is in use
lsof -ti:3000 | xargs kill -9

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS Error
Ensure backend `main.py` has:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### OpenAI API Error
- Check `.env` file has valid `OPENAI_API_KEY`
- Verify API key at https://platform.openai.com/api-keys
- Check account has credits

---

## 📚 Documentation

- **Backend**: `backend/RAG_IMPLEMENTATION.md`
- **Frontend**: `frontend/FRONTEND_SETUP.md`
- **Complete Guide**: `FRONTEND_COMPLETE.md`

---

## 🎓 Example Questions (Arabic)

- **Math**: "ما هو قانون فيثاغورس؟"
- **Physics**: "اشرح قانون نيوتن الثاني"
- **Chemistry**: "ما هي معادلة التفاعل الكيميائي؟"
- **With Image**: Upload image + "حل هذه المسألة"

---

## 🔄 Development Workflow

1. **Make Changes**: Edit files in `backend/` or `frontend/`
2. **Auto Reload**: Both servers support hot reload
3. **Test**: Refresh browser or test API endpoints
4. **Debug**: Check terminal logs for errors

---

## 🚀 Production Deployment

### Backend (Railway/Render/Fly.io)
```bash
cd backend
pip freeze > requirements.txt
# Deploy using platform CLI
```

### Frontend (Vercel/Netlify)
```bash
cd frontend
npm run build
# Deploy using platform CLI
```

---

## ✅ Verification Checklist

- [x] Backend server running on port 8000
- [x] Frontend server running on port 3000
- [x] TypeScript compilation successful
- [x] Production build successful
- [ ] OpenAI API key configured
- [ ] PDF curriculum uploaded
- [ ] Chat functionality tested
- [ ] LaTeX rendering verified

---

**Need Help?** Check the detailed documentation files or review the code comments.

**Last Updated**: 2025-11-19
