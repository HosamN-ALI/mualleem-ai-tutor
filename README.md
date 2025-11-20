# 🎓 Mualleem - Saudi Smart Math Tutor

**منصة تعليمية ذكية مدعومة بالذكاء الاصطناعي للطلاب السعوديين**

## 🇸🇦 النسخة العربية

### 📖 نظرة عامة
**معلّم** هو منصة تعليمية ذكية مدعومة بالذكاء الاصطناعي، مصممة خصيصاً لتقديم دروس رياضيات مخصصة للطلاب السعوديين، مع دعم كامل للغة العربية وتكامل سحابي مع **Qdrant Cloud** و **Requesty.ai**.

### ✅ حالة التثبيت الحالية (Installation Status)

- 🟢 **Backend (FastAPI + RAG + Qdrant Cloud + Requesty.ai)**:
  - تم إعداد البيئة وتشغيلها باستخدام ملف `.env` في مجلد `backend/` مع القيم:
    - `REQUESTY_API_KEY` و `REQUESTY_BASE_URL=https://router.requesty.ai/v1`
    - `SITE_URL=http://localhost:3000`
    - `SITE_NAME=Mualleem - AI Tutoring Platform`
    - `QDRANT_URL` و `QDRANT_API_KEY` و `QDRANT_COLLECTION_NAME=mualleem_curriculum`
  - تم التحقق من الاتصال بـ Qdrant Cloud عبر [`test_qdrant.py`](backend/test_qdrant.py:1) ومن تكامل Requesty.ai عبر [`test_requesty.py`](backend/test_requesty.py:1).
- 🟢 **Frontend (Next.js + Tailwind + TypeScript)**:
  - تم بناء وتشغيل واجهة الدردشة بنجاح كما هو موثّق في [`FRONTEND_COMPLETE.md`](FRONTEND_COMPLETE.md:1).
- 🟢 **تكامل Qdrant + Requesty.ai**:
  - موثّق بالكامل في:
    - [`QDRANT_SETUP_EN.md`](QDRANT_SETUP_EN.md:1) و[`README_QDRANT.md`](README_QDRANT.md:1)
    - [`REQUESTY_SETUP_COMPLETE.md`](REQUESTY_SETUP_COMPLETE.md:1) و[`REQUESTY_INTEGRATION.md`](REQUESTY_INTEGRATION.md:1)
- 🟢 **التشغيل من طرف لطرف (End-to-End)**:
  - يمكن حالياً:
    - رفع كتب PDF للمناهج عبر `/upload-curriculum`
    - طرح أسئلة نصية وصورية عبر `/chat`
    - استخدام واجهة الدردشة على `http://localhost:3000`

### 📂 وثائق التثبيت والتشغيل

- 🇸🇦 دليل التثبيت الكامل: [`INSTALLATION_GUIDE_AR.md`](INSTALLATION_GUIDE_AR.md:1)
- 🇸🇦 دليل إعداد المطوّر: [`DEVELOPER_GUIDE_AR.md`](DEVELOPER_GUIDE_AR.md:1)
- 🇸🇦 دليل التشغيل والعمليات: [`OPERATIONAL_GUIDE_AR.md`](OPERATIONAL_GUIDE_AR.md:1)

### ✨ المميزات
- 🤖 معلم ذكاء اصطناعي يعتمد على نماذج OpenAI عبر Requesty.ai (مثل `openai/gpt-4o` و `openai/gpt-4o-mini`)
- 📚 محرك RAG يعتمد على Qdrant Cloud لتخزين وفهرسة المناهج الدراسية
- 🔍 دعم الأسئلة النصية والصورية (Vision) عبر `/chat`
- 🧮 عرض المعادلات الرياضية بصيغة LaTeX في واجهة الدردشة
- 🇸🇦 دعم اللغة العربية الكامل (RTL + واجهة عربية)

### 🚀 البدء السريع (ملخّص)

لبيئة تطوير محلية بعد استكمال الإعداد كما في دليل التثبيت:

```bash
# 1. تشغيل Backend (من مجلد backend)
cd backend
python3 main.py

# 2. تشغيل Frontend (من مجلد frontend)
cd ../frontend
npm install   # مرة واحدة فقط عند أول تشغيل
npm run dev
```

- Backend: متوفّر على `http://localhost:8000`
- Frontend: متوفّر على `http://localhost:3000`

للتفاصيل الكاملة راجع: [`INSTALLATION_GUIDE_AR.md`](INSTALLATION_GUIDE_AR.md:1).

## 🇬🇧 English Version

### 📖 Overview
**Mualleem** is an AI-powered educational platform for Saudi students, using:
- **FastAPI** backend with **Qdrant Cloud** for vector search
- **Requesty.ai** as the unified AI gateway (OpenAI-compatible)
- **Next.js** frontend with an Arabic-first chat interface

### ✨ Features
- 🤖 AI Tutor with GPT-4o / GPT-4o-mini via Requesty.ai
- 📚 RAG Engine powered by Qdrant Cloud
- 🔍 OCR / Vision support for math problems (images)
- 🧮 LaTeX math rendering in the chat UI
- 🇸🇦 Full Arabic and RTL support

### 🔧 Tech Stack
- Backend: FastAPI, Qdrant Cloud, Requesty.ai (OpenAI-compatible SDK)
- Frontend: Next.js, TypeScript, Tailwind CSS, React components for chat and LaTeX

---
**Made with ❤️ for Saudi Students**
