# 🚀 Requesty.ai Integration Guide

## Overview
تم تكوين منصة معلّم لاستخدام **Requesty.ai** كبوابة موحدة للوصول إلى أكثر من 300 نموذج ذكاء اصطناعي مع تحسين التكلفة والأداء.

Your Mualleem platform is now configured to use **Requesty.ai** as a unified AI gateway, providing access to 300+ AI models with built-in optimization, caching, and cost tracking.

---

## ✅ Configuration Status

### API Credentials
- **API Key**: `rqsty-sk-y4aKgcDPSLuXh6PXd4vHGBtHPlWRkyfZVcN6R3thk+7q8djI+bZs0L98Ud0PdZr0rsx1M/N1AGP07BZDhyeDSfVyyhum2Hbf6uVTPyFN8wU=`
- **Base URL**: `https://router.requesty.ai/v1`
- **Site URL**: `http://localhost:3000`
- **Site Name**: `Mualleem - AI Tutoring Platform`

### Models in Use
1. **Chat Completion**:
   - `openai/gpt-4o` - For vision tasks (image + text)
   - `openai/gpt-4o-mini` - For text-only questions (cost-effective)

2. **Embeddings**:
   - `openai/text-embedding-3-small` - For RAG (supports Arabic)

---

## 📁 Updated Files

### 1. `/backend/.env`
```env
REQUESTY_API_KEY=rqsty-sk-y4aKgcDPSLuXh6PXd4vHGBtHPlWRkyfZVcN6R3thk+7q8djI+bZs0L98Ud0PdZr0rsx1M/N1AGP07BZDhyeDSfVyyhum2Hbf6uVTPyFN8wU=
REQUESTY_BASE_URL=https://router.requesty.ai/v1
SITE_URL=http://localhost:3000
SITE_NAME=Mualleem - AI Tutoring Platform
```

### 2. `/backend/rag_service.py`
- ✅ OpenAI client initialized with Requesty.ai base URL
- ✅ Custom headers added (`HTTP-Referer`, `X-Title`)
- ✅ Model format updated to `provider/model` (e.g., `openai/gpt-4o`)

### 3. `/backend/main.py`
- ✅ Chat endpoint uses `openai/gpt-4o` for vision
- ✅ Chat endpoint uses `openai/gpt-4o-mini` for text-only
- ✅ Model names returned in API responses updated

---

## 🧪 Testing the Integration

### Run the Test Script
```bash
cd backend
python test_requesty.py
```

**Expected Output:**
```
🔍 Testing Requesty.ai Configuration...

✓ API Key: rqsty-sk-y4aKgcDPSL...N8wU=
✓ Base URL: https://router.requesty.ai/v1
✓ Site URL: http://localhost:3000
✓ Site Name: Mualleem

📡 Testing Chat Completion (GPT-4o-mini)...
✅ Chat Response: مرحباً! كيف يمكنني مساعدتك اليوم؟

📊 Testing Embeddings (text-embedding-3-small)...
✅ Embedding Generated: 1536 dimensions

🎉 All tests passed! Requesty.ai is configured correctly.
```

---

## 🔧 How It Works

### Client Initialization (rag_service.py)
```python
from openai import OpenAI

client = OpenAI(
    api_key=requesty_api_key,
    base_url="https://router.requesty.ai/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Mualleem - AI Tutoring Platform"
    }
)
```

### Chat Completion Example
```python
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",  # Note: provider/model format
    messages=[
        {"role": "user", "content": "ما هو حل المعادلة x + 5 = 10؟"}
    ]
)
```

### Embeddings Example
```python
response = client.embeddings.create(
    model="openai/text-embedding-3-small",
    input=["النص العربي للتضمين"]
)
```

---

## 💡 Benefits of Requesty.ai

1. **Unified Gateway**: Access 300+ models through one API
2. **Cost Optimization**: Automatic routing to cost-effective models
3. **Caching**: Built-in response caching for repeated queries
4. **Monitoring**: Track usage and costs in the Requesty dashboard
5. **Fallback**: Automatic failover if a model is unavailable
6. **Arabic Support**: Full support for RTL languages

---

## 🚀 Next Steps

### 1. Start the Backend Server
```bash
cd backend
python -m pip install -r requirements.txt
python main.py
```

### 2. Test the API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Chat Request:**
```bash
curl -X POST http://localhost:8000/chat \
  -F "question=ما هو 2 + 2؟"
```

### 3. Monitor Usage
Visit [app.requesty.ai](https://app.requesty.ai) to:
- View API usage statistics
- Track costs per model
- Monitor response times
- Set up alerts and limits

---

## 🔒 Security Notes

1. **API Key Protection**: Never commit `.env` file to git
2. **Environment Variables**: Always load from `.env` in production
3. **Rate Limiting**: Requesty.ai handles rate limiting automatically
4. **HTTPS**: All requests are encrypted via HTTPS

---

## 📚 Additional Resources

- [Requesty.ai Documentation](https://docs.requesty.ai)
- [OpenAI SDK Compatibility](https://docs.requesty.ai/integration/openai-sdk)
- [Model Pricing](https://app.requesty.ai/pricing)
- [API Reference](https://docs.requesty.ai/api-reference)

---

## ❓ Troubleshooting

### Error: "Invalid API Key"
- Verify the API key in `.env` file
- Check for extra spaces or line breaks
- Regenerate key at app.requesty.ai

### Error: "Model not found"
- Ensure model format is `provider/model` (e.g., `openai/gpt-4o`)
- Check available models at app.requesty.ai

### Error: "Connection timeout"
- Check internet connection
- Verify base URL: `https://router.requesty.ai/v1`
- Check firewall settings

---

## 📞 Support

For issues or questions:
- **Requesty Support**: support@requesty.ai
- **Documentation**: https://docs.requesty.ai
- **Dashboard**: https://app.requesty.ai

---

**تم التكوين بنجاح! ✅**
**Configuration Complete! ✅**
