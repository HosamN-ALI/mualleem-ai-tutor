# 🎓 Mualleem - معلّم | AI-Powered Arabic Tutoring Platform

<div dir="rtl">

## 📖 نظرة عامة

**معلّم** هي منصة تعليمية ذكية مدعومة بالذكاء الاصطناعي، مصممة خصيصاً للطلاب العرب. تتيح المنصة للطلاب التفاعل مع كتبهم الدراسية من خلال:
- 📸 رفع صور للمسائل الرياضية والعلمية
- 💬 طرح أسئلة نصية بناءً على المنهج الدراسي
- 🤖 الحصول على شروحات تفصيلية خطوة بخطوة باللغة العربية

</div>

---

## 🚀 المميزات الرئيسية

- ✅ **دعم الرؤية (Vision)**: رفع صور المسائل والحصول على حلول فورية
- ✅ **RAG (Retrieval-Augmented Generation)**: البحث الذكي في المناهج الدراسية المرفوعة
- ✅ **عرض المعادلات الرياضية**: دعم LaTeX لعرض المعادلات بشكل احترافي
- ✅ **واجهة عربية**: دعم كامل للغة العربية مع RTL
- ✅ **قاعدة بيانات متجهات سحابية**: استخدام Qdrant Cloud للأداء العالي
- ✅ **نموذج AI متقدم**: استخدام GPT-4o عبر Requesty.ai

---

## 🛠️ التقنيات المستخدمة

### Backend
- **Python 3.11+** - لغة البرمجة الأساسية
- **FastAPI** - إطار عمل API سريع وحديث
- **Qdrant Cloud** - قاعدة بيانات متجهات سحابية
- **Requesty.ai** - بوابة موحدة لنماذج الذكاء الاصطناعي
- **GPT-4o** - نموذج OpenAI للرؤية والنصوص

### Frontend
- **Next.js 14+** - إطار عمل React مع App Router
- **Tailwind CSS** - تصميم عصري وسريع
- **TypeScript** - لغة برمجة آمنة من الأخطاء
- **React KaTeX** - عرض المعادلات الرياضية

---

## 📁 هيكل المشروع

```
mualleem-ai-tutor/
├── backend/                 # خادم FastAPI
│   ├── main.py             # نقطة الدخول الرئيسية
│   ├── rag_service.py      # خدمة RAG
│   ├── rag_engine.py       # محرك البحث
│   ├── requirements.txt    # المكتبات المطلوبة
│   └── data/               # المناهج الدراسية (PDF)
│
├── frontend/               # تطبيق Next.js
│   ├── app/               # App Router
│   ├── components/        # مكونات React
│   └── package.json       # المكتبات المطلوبة
│
└── docs/                  # التوثيق
```

---

## 🚀 التثبيت والتشغيل

### المتطلبات الأساسية
- Python 3.11+
- Node.js 18+
- npm أو yarn

### 1️⃣ تثبيت Backend

```bash
cd backend

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Linux/Mac
# أو
venv\Scripts\activate     # على Windows

# تثبيت المكتبات
pip install -r requirements.txt

# إعداد المتغيرات البيئية
cp .env.example .env
# قم بتعديل .env وإضافة مفاتيح API

# تشغيل الخادم
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2️⃣ تثبيت Frontend

```bash
cd frontend

# تثبيت المكتبات
npm install

# تشغيل التطبيق
npm run dev
```

### 3️⃣ الوصول للتطبيق

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🔑 المتغيرات البيئية

### Backend (.env)

```env
# Requesty.ai API
REQUESTY_API_KEY=your_requesty_api_key_here
REQUESTY_BASE_URL=https://router.requesty.ai/v1

# Qdrant Cloud
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Model Configuration
MODEL_NAME=openai/gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
```

---

## 📚 الاستخدام

### 1. رفع منهج دراسي (PDF)

```bash
curl -X POST "http://localhost:8000/upload-curriculum" \
  -F "file=@path/to/textbook.pdf"
```

### 2. طرح سؤال نصي

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "ما هو قانون نيوتن الثاني؟"}'
```

### 3. رفع صورة مسألة

```bash
curl -X POST "http://localhost:8000/chat" \
  -F "question=حل هذه المسألة" \
  -F "image=@problem.jpg"
```

---

## 🧪 الاختبار

### اختبار Backend

```bash
cd backend

# اختبار الاتصال بـ Requesty.ai
python test_requesty.py

# اختبار الاتصال بـ Qdrant
python test_qdrant.py

# اختبار RAG Engine
python test_rag.py
```

---

## 📖 التوثيق الإضافي

- [دليل التشغيل السريع](./QUICK_START.md)
- [دليل إعداد Qdrant](./QDRANT_SETUP_COMPLETE.md)
- [دليل تكامل Requesty](./REQUESTY_INTEGRATION.md)
- [البنية المعمارية](./ARCHITECTURE.md)

---

## 🤝 المساهمة

نرحب بمساهماتكم! يرجى:
1. عمل Fork للمشروع
2. إنشاء فرع جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للفرع (`git push origin feature/amazing-feature`)
5. فتح Pull Request

---

## 📄 الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE)

---

## 👨‍💻 المطور

تم تطوير هذا المشروع بواسطة **HosamN-ALI**

- GitHub: [@HosamN-ALI](https://github.com/HosamN-ALI)

---

## 🙏 شكر وتقدير

- [OpenAI](https://openai.com) - نماذج GPT-4o
- [Requesty.ai](https://requesty.ai) - بوابة AI موحدة
- [Qdrant](https://qdrant.tech) - قاعدة بيانات المتجهات
- [FastAPI](https://fastapi.tiangolo.com) - إطار عمل Python
- [Next.js](https://nextjs.org) - إطار عمل React

---

<div align="center">

**صُنع بـ ❤️ للطلاب العرب**

⭐ إذا أعجبك المشروع، لا تنسى إعطاءه نجمة!

</div>
