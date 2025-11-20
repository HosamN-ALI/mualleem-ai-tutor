# 🎓 معلّم - منصة التعليم بالذكاء الاصطناعي

## نظرة عامة

**معلّم** هي منصة تعليمية ذكية تستخدم الذكاء الاصطناعي لمساعدة الطلاب العرب في فهم المناهج الدراسية. يمكن للطلاب رفع صور للمسائل أو طرح أسئلة نصية والحصول على شروحات مفصلة خطوة بخطوة بالعربية.

---

## ✨ الميزات الرئيسية

- 📚 **رفع المناهج**: رفع ملفات PDF للمناهج الدراسية
- 🔍 **البحث الذكي**: RAG (Retrieval-Augmented Generation)
- 💬 **محادثة ذكية**: أسئلة نصية مع سياق من المنهج
- 📸 **تحليل الصور**: رفع صور للمسائل والحصول على حلول
- 🧮 **دعم LaTeX**: عرض المعادلات الرياضية بشكل احترافي
- 🇸🇦 **دعم العربية**: واجهة وشروحات بالعربية الفصحى
- ☁️ **سحابي**: Qdrant Cloud للتخزين
- 🚀 **سريع**: Requesty.ai للذكاء الاصطناعي

---

## 🏗️ البنية التقنية

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **AI Gateway**: Requesty.ai
- **Vector DB**: Qdrant Cloud
- **Models**:
  - `openai/gpt-4o` - للرؤية والنصوص
  - `openai/gpt-4o-mini` - للنصوص
  - `openai/text-embedding-3-small` - للتضمينات

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Styling**: Tailwind CSS
- **Math Rendering**: react-katex
- **RTL Support**: دعم كامل للعربية

---

## 🚀 البدء السريع

### المتطلبات
- Python 3.11+
- Node.js 18+
- pip
- npm/yarn

### 1. تثبيت Backend

```bash
# الانتقال إلى مجلد Backend
cd backend

# تثبيت التبعيات
pip install -r requirements.txt

# تشغيل الخادم
python3 main.py
```

الخادم سيعمل على: `http://localhost:8000`

### 2. تثبيت Frontend (إذا كان متوفراً)

```bash
# الانتقال إلى مجلد Frontend
cd frontend

# تثبيت التبعيات
npm install

# تشغيل التطبيق
npm run dev
```

التطبيق سيعمل على: `http://localhost:3000`

---

## 🔧 التكوين

### ملف .env (Backend)

```env
# Requesty.ai Configuration
REQUESTY_API_KEY=your_requesty_api_key_here
REQUESTY_BASE_URL=https://router.requesty.ai/v1

# Qdrant Cloud Configuration
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=curriculum_collection

# Site Information
SITE_URL=http://localhost:3000
SITE_NAME=Mualleem

# Server Configuration
PORT=8000
HOST=0.0.0.0
```

---

## 📡 API Endpoints

### 1. الصفحة الرئيسية
```http
GET /
```

**Response**:
```json
{
  "message": "مرحباً بك في منصة معلّم التعليمية",
  "status": "active"
}
```

### 2. فحص الصحة
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "service": "Mualleem Backend"
}
```

### 3. الإحصائيات
```http
GET /stats
```

**Response**:
```json
{
  "collection_name": "curriculum_collection",
  "total_chunks": 150,
  "vector_size": 1536,
  "status": "active",
  "storage": "Qdrant Cloud"
}
```

### 4. رفع منهج دراسي
```http
POST /upload-curriculum
Content-Type: multipart/form-data

file: [PDF file]
```

**Response**:
```json
{
  "message": "تم رفع المنهج وفهرسته بنجاح",
  "filename": "textbook.pdf",
  "total_chunks": 150,
  "total_characters": 125000,
  "status": "indexed"
}
```

### 5. المحادثة
```http
POST /chat
Content-Type: multipart/form-data

question: "ما هي نظرية فيثاغورس؟"
image: [optional image file]
```

**Response**:
```json
{
  "answer": "نظرية فيثاغورس تنص على أن مربع طول الوتر...",
  "question": "ما هي نظرية فيثاغورس؟",
  "has_image": false,
  "context_used": true,
  "model_used": "openai/gpt-4o-mini",
  "provider": "Requesty.ai Gateway"
}
```

---

## 🧪 الاختبار

### اختبار الاتصال بـ Qdrant Cloud
```bash
cd backend
python3 test_qdrant.py
```

### اختبار RAG Service
```bash
cd backend
python3 -c "from rag_service import rag_service; print(rag_service.get_collection_stats())"
```

### اختبار API
```bash
# فحص الصحة
curl http://localhost:8000/health

# الإحصائيات
curl http://localhost:8000/stats

# رفع منهج
curl -X POST http://localhost:8000/upload-curriculum \
  -F "file=@textbook.pdf"

# سؤال
curl -X POST http://localhost:8000/chat \
  -F "question=ما هي نظرية فيثاغورس؟"
```

---

## 📁 هيكل المشروع

```
mualleem/
├── backend/
│   ├── .env                    # متغيرات البيئة
│   ├── main.py                 # FastAPI application
│   ├── rag_service.py          # RAG logic (Qdrant)
│   ├── rag_engine.py           # Alternative RAG
│   ├── requirements.txt        # Python dependencies
│   ├── test_qdrant.py         # Qdrant test
│   └── data/                   # PDF storage
│
├── frontend/
│   ├── app/                    # Next.js app directory
│   ├── components/             # React components
│   ├── public/                 # Static files
│   └── package.json            # Node dependencies
│
├── QDRANT_MIGRATION.md         # دليل الترحيل
├── QDRANT_QUICKSTART.md        # البدء السريع
├── QDRANT_SETUP_COMPLETE.md    # ملخص الإعداد
└── README_QDRANT.md            # هذا الملف
```

---

## 🔍 كيف يعمل النظام؟

### 1. رفع المنهج
```
PDF → استخراج النص → تقسيم إلى chunks → 
توليد embeddings → تخزين في Qdrant Cloud
```

### 2. الإجابة على سؤال
```
سؤال المستخدم → توليد embedding → 
البحث في Qdrant → استرجاع السياق → 
إرسال إلى GPT-4o → توليد الإجابة
```

### 3. تحليل صورة
```
صورة + سؤال → استرجاع السياق → 
إرسال إلى GPT-4o Vision → تحليل الصورة → 
توليد الإجابة مع الشرح
```

---

## 🎯 حالات الاستخدام

### للطلاب
- ✅ فهم المفاهيم الصعبة
- ✅ حل الواجبات المنزلية
- ✅ التحضير للامتحانات
- ✅ مراجعة الدروس

### للمعلمين
- ✅ إنشاء محتوى تعليمي
- ✅ توليد أمثلة وتمارين
- ✅ شرح المفاهيم بطرق مختلفة

---

## 🔐 الأمان والخصوصية

- 🔒 جميع API Keys مشفرة
- 🔒 اتصال HTTPS مع Qdrant Cloud
- 🔒 لا يتم تخزين بيانات المستخدمين
- 🔒 CORS محدد للـ frontend فقط

---

## 📊 الأداء

| العملية | الوقت المتوقع |
|---------|---------------|
| رفع PDF (100 صفحة) | ~30-60 ثانية |
| البحث في Qdrant | < 100ms |
| توليد الإجابة | 2-5 ثواني |
| تحليل صورة | 3-7 ثواني |

---

## 🛠️ استكشاف الأخطاء

### المشكلة: خطأ في الاتصال بـ Qdrant
```bash
# اختبار الاتصال
cd backend
python3 test_qdrant.py
```

### المشكلة: خطأ في Requesty.ai
```bash
# التحقق من API Key
cd backend
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('REQUESTY_API_KEY'))"
```

### المشكلة: خطأ في رفع PDF
```bash
# التحقق من مجلد data
mkdir -p backend/data
chmod 755 backend/data
```

---

## 📚 الموارد والمراجع

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Requesty.ai Docs](https://docs.requesty.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:
1. Fork المشروع
2. إنشاء branch جديد
3. Commit التغييرات
4. Push إلى Branch
5. فتح Pull Request

---

## 📝 الترخيص

هذا المشروع مفتوح المصدر ومتاح للاستخدام التعليمي.

---

## 📞 التواصل

لأي استفسارات أو مشاكل، يرجى فتح Issue على GitHub.

---

## 🎉 شكر خاص

- OpenAI لنماذج GPT-4
- Qdrant لقاعدة البيانات المتجهة
- Requesty.ai للبوابة الموحدة
- المجتمع العربي للدعم المستمر

---

**صُنع بـ ❤️ للطلاب العرب**

**الإصدار**: 2.0 (Qdrant Cloud Edition)  
**آخر تحديث**: 20 نوفمبر 2025
