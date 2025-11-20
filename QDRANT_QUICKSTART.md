# 🚀 دليل البدء السريع - Qdrant Cloud

## ✅ تم التكوين بنجاح!

تم تحديث منصة معلّم لاستخدام **Qdrant Cloud** و **Requesty.ai**

---

## 📋 الخطوات التالية

### 1️⃣ تثبيت التبعيات
```bash
cd backend
pip install -r requirements.txt
```

### 2️⃣ تشغيل الخادم
```bash
cd backend
python3 main.py
```

أو باستخدام uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3️⃣ اختبار الخادم
افتح متصفح جديد وانتقل إلى:
```
http://localhost:8000
```

يجب أن ترى:
```json
{
  "message": "مرحباً بك في منصة معلّم التعليمية",
  "status": "active"
}
```

### 4️⃣ فحص الإحصائيات
```bash
curl http://localhost:8000/stats
```

النتيجة المتوقعة:
```json
{
  "collection_name": "curriculum_collection",
  "total_chunks": 0,
  "vector_size": 1536,
  "status": "active",
  "storage": "Qdrant Cloud"
}
```

---

## 📤 رفع منهج دراسي (PDF)

### باستخدام curl:
```bash
curl -X POST http://localhost:8000/upload-curriculum \
  -F "file=@/path/to/your/textbook.pdf"
```

### باستخدام Postman:
1. اختر `POST` request
2. URL: `http://localhost:8000/upload-curriculum`
3. Body → form-data
4. Key: `file` (نوع: File)
5. Value: اختر ملف PDF

### النتيجة المتوقعة:
```json
{
  "message": "تم رفع المنهج وفهرسته بنجاح",
  "filename": "textbook.pdf",
  "total_chunks": 150,
  "total_characters": 125000,
  "status": "indexed"
}
```

---

## 💬 اختبار المحادثة

### سؤال نصي فقط:
```bash
curl -X POST http://localhost:8000/chat \
  -F "question=ما هي نظرية فيثاغورس؟"
```

### سؤال مع صورة:
```bash
curl -X POST http://localhost:8000/chat \
  -F "question=حل هذه المسألة" \
  -F "image=@/path/to/math_problem.jpg"
```

### النتيجة المتوقعة:
```json
{
  "answer": "نظرية فيثاغورس تنص على أن...",
  "question": "ما هي نظرية فيثاغورس؟",
  "has_image": false,
  "context_used": true,
  "model_used": "openai/gpt-4o-mini",
  "provider": "Requesty.ai Gateway"
}
```

---

## 🔧 التكوين الحالي

### ✅ Qdrant Cloud
- **URL**: `https://dfc1c80b-b7f2-4b4f-8daa-1582a8b80e3e.europe-west3-0.gcp.cloud.qdrant.io:6333`
- **Region**: Europe West 3 (GCP)
- **Collection**: `curriculum_collection`
- **Vector Size**: 1536 (text-embedding-3-small)
- **Distance**: COSINE

### ✅ Requesty.ai
- **Base URL**: `https://router.requesty.ai/v1`
- **Models**: 
  - `openai/gpt-4o` (للصور والنصوص)
  - `openai/gpt-4o-mini` (للنصوص فقط)
  - `openai/text-embedding-3-small` (للـ embeddings)

---

## 🧪 اختبار الاتصال

### اختبار Qdrant Cloud:
```bash
cd backend
python3 test_qdrant.py
```

النتيجة المتوقعة:
```
✅ Successfully connected to Qdrant Cloud!
✅ Collection 'curriculum_collection' exists
   📊 Points: 0
   📐 Vector Size: 1536
   📏 Distance: Cosine
✅ All tests passed!
```

### اختبار RAG Service:
```bash
cd backend
python3 -c "from rag_service import rag_service; print(rag_service.get_collection_stats())"
```

---

## 📁 هيكل المشروع

```
backend/
├── .env                    # متغيرات البيئة (Qdrant + Requesty)
├── main.py                 # FastAPI server
├── rag_service.py          # RAG logic (Qdrant Cloud)
├── rag_engine.py           # Alternative RAG implementation
├── requirements.txt        # Python dependencies
├── test_qdrant.py         # Qdrant connection test
└── data/                   # PDF files storage
```

---

## 🔍 استكشاف الأخطاء

### ❌ خطأ: "QDRANT_URL not set"
**الحل**: تأكد من وجود ملف `.env` في مجلد `backend` مع جميع المتغيرات

### ❌ خطأ: "Connection refused"
**الحل**: تحقق من URL و API Key في ملف `.env`

### ❌ خطأ: "REQUESTY_API_KEY not set"
**الحل**: أضف `REQUESTY_API_KEY` إلى ملف `.env`

### ❌ خطأ: "Collection not found"
**الحل**: سيتم إنشاء Collection تلقائياً عند أول استخدام

---

## 📊 مراقبة الأداء

### عرض عدد المستندات المفهرسة:
```bash
curl http://localhost:8000/stats
```

### عرض جميع Collections في Qdrant:
```bash
python3 test_qdrant.py
```

---

## 🎯 الميزات المتاحة

- ✅ رفع وفهرسة ملفات PDF
- ✅ البحث الدلالي (Semantic Search)
- ✅ الإجابة على الأسئلة النصية
- ✅ تحليل الصور (Vision)
- ✅ شرح خطوة بخطوة بالعربية
- ✅ دعم LaTeX للمعادلات الرياضية
- ✅ RAG (Retrieval-Augmented Generation)

---

## 📚 الموارد المفيدة

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Requesty.ai Docs](https://docs.requesty.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 🎉 جاهز للاستخدام!

الآن يمكنك:
1. ✅ رفع منهج دراسي (PDF)
2. ✅ طرح أسئلة نصية
3. ✅ رفع صور للمسائل
4. ✅ الحصول على شروحات مفصلة بالعربية

**استمتع بمنصة معلّم! 🚀**

---

**آخر تحديث**: 20 نوفمبر 2025
