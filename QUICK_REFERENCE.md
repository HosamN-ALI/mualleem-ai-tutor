# 🚀 Requesty.ai Quick Reference

## ⚡ Quick Start

```bash
# 1. Start Backend
cd backend
source venv/bin/activate
python3 main.py

# 2. Test Integration
python3 test_requesty.py

# 3. Start Frontend (in new terminal)
cd frontend
npm run dev
```

## 🔑 API Key Configuration

**File**: `backend/.env`
```env
REQUESTY_API_KEY=rqsty-sk-y4aKgcDPSLuXh6PXd4vHGBtHPlWRkyfZVcN6R3thk+7q8djI+bZs0L98Ud0PdZr0rsx1M/N1AGP07BZDhyeDSfVyyhum2Hbf6uVTPyFN8wU=
REQUESTY_BASE_URL=https://router.requesty.ai/v1
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Health check |
| `/stats` | GET | Collection stats |
| `/upload-curriculum` | POST | Upload PDF textbook |
| `/chat` | POST | Ask question (text + image) |

## 🤖 Models Used

| Purpose | Model | When |
|---------|-------|------|
| Text Chat | `openai/gpt-4o-mini` | Text-only questions |
| Vision | `openai/gpt-4o` | Image + text questions |
| Embeddings | `openai/text-embedding-3-small` | PDF indexing |

## 📝 Example Requests

### Text Question
```bash
curl -X POST http://localhost:8000/chat \
  -F "question=اشرح نظرية فيثاغورس"
```

### Image Question
```bash
curl -X POST http://localhost:8000/chat \
  -F "question=حل هذه المسألة" \
  -F "image=@problem.jpg"
```

### Upload PDF
```bash
curl -X POST http://localhost:8000/upload-curriculum \
  -F "file=@textbook.pdf"
```

## 🔍 Testing

```bash
# Quick test
cd backend
python3 test_requesty.py
```

## 📊 Monitoring

**Dashboard**: https://app.requesty.ai

**Metrics**:
- Real-time usage
- Cost tracking
- Request logs
- Performance analytics

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| API Key not found | Check `.env` file exists and has `REQUESTY_API_KEY` |
| Connection timeout | Verify internet connection and firewall |
| Model not found | Use `provider/model` format (e.g., `openai/gpt-4o`) |
| Import error | Run `pip install -r requirements.txt` |

## 📚 Documentation

- [Full Integration Guide](./REQUESTY_INTEGRATION.md)
- [Arabic Guide](./REQUESTY_ARABIC.md)
- [Architecture](./ARCHITECTURE.md)
- [Setup Complete](./REQUESTY_SETUP_COMPLETE.md)

## ✅ Status

- **Integration**: ✅ Complete
- **Testing**: ✅ Passed
- **Documentation**: ✅ Complete
- **Ready**: ✅ Production

---

**Last Updated**: November 20, 2025  
**Version**: 1.0
