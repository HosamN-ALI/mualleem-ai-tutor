# 📥 دليل التثبيت الكامل لمنصة «معلّم» (Mualleem AI Tutor)

> **ملاحظة**: هذا الدليل يفترض أنك تقوم بالتثبيت على بيئة تطوير محلية (Developer Machine) باستخدام **Backend (FastAPI + Qdrant + Requesty.ai)** و **Frontend (Next.js)**، مع الاعتماد على **Qdrant Cloud** و **Requesty.ai** كخدمات سحابية جاهزة.

---

## 1. ✅ المتطلبات النظامية (System Requirements)

### 1.1 متطلبات العتاد (Hardware)

- معالج حديث (Intel i5 / Ryzen 5 أو أعلى)
- ذاكرة RAM لا تقل عن **8GB** (يفضّل 16GB لتجربة أفضل)
- مساحة تخزين فارغة لا تقل عن **5GB** (لبيئة Python + Node + ملفات المناهج PDF)

### 1.2 متطلبات النظام (Operating System)

- Linux (موصى به – مثال: Ubuntu 20.04+)
- أو macOS 12+
- أو Windows 10/11 (مع WSL2 مفضّل للعمل بسلاسة مع Python وNode)

### 1.3 المتطلبات البرمجية (Software Dependencies)

#### Backend

- **Python 3.11+**
- أداة إدارة الحزم: `pip` أو `pip3`
- إمكانية إنشاء بيئة افتراضية `venv`

#### Frontend

- **Node.js 18+**
- **npm 9+** (أو **pnpm/yarn** إذا رغبت، لكن السكربتات في المشروع تستخدم `npm`)

#### خدمات سحابية (Cloud Services)

1. **Qdrant Cloud**  
   - حساب مفعّل على: https://cloud.qdrant.io  
   - **QDRANT_URL**
   - **QDRANT_API_KEY**
   - **QDRANT_COLLECTION_NAME** (مثل: `mualleem_curriculum`)

2. **Requesty.ai**  
   - حساب مفعّل على: https://app.requesty.ai  
   - **REQUESTY_API_KEY**
   - **REQUESTY_BASE_URL** = `https://router.requesty.ai/v1`
   - معلومات تعريف الموقع:
     - **SITE_URL** = `http://localhost:3000`
     - **SITE_NAME** = `Mualleem - AI Tutoring Platform`

---

## 2. 📁 تحميل المشروع وتجهيز المجلدات

1. استنساخ المستودع (Git Clone):

```bash
cd /path/to/workspace
git clone <REPO_URL> mualleem-ai-tutor
cd mualleem-ai-tutor
```

2. هيكل المشروع الرئيسي:

```text
mualleem-ai-tutor/
├── backend/          # خادم FastAPI وRAG
└── frontend/         # تطبيق Next.js (واجهة المستخدم)
```

---

## 3. ⚙️ إعداد الـ Backend (FastAPI + Qdrant + Requesty.ai)

### 3.1 إنشاء وتفعيل بيئة Python افتراضية

من داخل مجلد المشروع:

```bash
cd backend

# إنشاء بيئة افتراضية
python3 -m venv .venv

# تفعيل البيئة (Linux/macOS)
source .venv/bin/activate

# (على Windows PowerShell)
# .venv\Scripts\Activate.ps1
```

### 3.2 تثبيت التبعيات (Python Requirements)

```bash
cd backend
pip install -r requirements.txt
```

سيتضمن ذلك مكتبات مثل:

- `fastapi`
- `uvicorn`
- `qdrant-client`
- `openai` (مستخدمة عبر بوابة Requesty.ai)
- مكتبات مساعدة أخرى

### 3.3 إعداد متغيرات البيئة (Environment Variables)

يستخدم الـ Backend ملف `.env` داخل مجلد `backend/` لتجميع إعدادات Qdrant وRequesty.ai وغيرها.

#### 3.3.1 إنشاء ملف `.env`

من داخل `backend/`:

```bash
cd backend
cat > .env << 'EOF'
REQUESTY_API_KEY=your_requesty_api_key_here
REQUESTY_BASE_URL=https://router.requesty.ai/v1

SITE_URL=http://localhost:3000
SITE_NAME=Mualleem - AI Tutoring Platform

PORT=8000
HOST=0.0.0.0

QDRANT_URL=https://YOUR-QDRANT-URL:6333
QDRANT_COLLECTION_NAME=mualleem_curriculum
QDRANT_API_KEY=YOUR_QDRANT_API_KEY
EOF
```

ثم عدّل القيم التالية بالقيم الفعلية من حساباتك:

- `REQUESTY_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
- (يمكنك الإبقاء على `QDRANT_COLLECTION_NAME=mualleem_curriculum` كما هي، أو تغييرها بما يناسبك)

#### 3.3.2 مثال على إعداد فعلي (للمرجع فقط)

موضّح في بعض ملفات التوثيق الداخلية مثل:

```env
QDRANT_URL=https://dfc1c80b-b7f2-4b4f-8daa-1582a8b80e3e.europe-west3-0.gcp.cloud.qdrant.io:6333
QDRANT_COLLECTION_NAME=mualleem_curriculum
REQUESTY_BASE_URL=https://router.requesty.ai/v1
SITE_URL=http://localhost:3000
SITE_NAME=Mualleem - AI Tutoring Platform
```

> **تحذير أمني**:  
> لا تضف ملف `.env` إلى Git أو أي مستودع عام، لأنّه يحتوي على مفاتيح سرّية.

### 3.4 اختبار الاتصال بـ Qdrant Cloud

لتأكيد إعداد Qdrant:

```bash
cd backend
python3 test_qdrant.py
```

**متوقّع:**

```text
✅ Successfully connected to Qdrant Cloud!
✅ Collection 'curriculum_collection' exists (أو تم إنشاؤها)
✅ All tests passed!
```

إن ظهرت أخطاء، راجع دليل [`QDRANT_SETUP_EN.md`](mualleem-ai-tutor/QDRANT_SETUP_EN.md:1) ودليل [`QDRANT_QUICKSTART.md`](mualleem-ai-tutor/QDRANT_QUICKSTART.md).

### 3.5 اختبار تكامل Requesty.ai

لتأكيد إعداد Requesty.ai:

```bash
cd backend
python3 test_requesty.py
```

**متوقّع (بتقريب):**

```text
🔍 Testing Requesty.ai Configuration...

✓ API Key: rqsty-sk-...
✓ Base URL: https://router.requesty.ai/v1
✓ Site URL: http://localhost:3000
✓ Site Name: Mualleem - AI Tutoring Platform

📡 Testing Chat Completion (GPT-4o-mini)...
✅ Chat Response: مرحباً! كيف يمكنني مساعدتك اليوم؟

📊 Testing Embeddings (text-embedding-3-small)...
✅ Embedding Generated: 1536 dimensions

🎉 All tests passed! Requesty.ai is configured correctly.
```

تفاصيل أكثر في [`REQUESTY_SETUP_COMPLETE.md`](mualleem-ai-tutor/REQUESTY_SETUP_COMPLETE.md:1).

### 3.6 تشغيل خادم الـ Backend

بعد نجاح الاختبارات السابقة:

```bash
cd backend
# إذا لم تكن البيئة مفعّلة:
# source .venv/bin/activate

python3 main.py
# أو:
# uvicorn main:app --host 0.0.0.0 --port 8000
```

**متوقّع في السجل (Logs):**

```text
✓ Initialized Requesty.ai client
✓ Connected to Qdrant Cloud
INFO:     Uvicorn running on http://0.0.0.0:8000
```

الآن يكون الـ Backend متوفّر على:  
`http://localhost:8000`

---

## 4. 💻 إعداد الـ Frontend (Next.js)

### 4.1 تثبيت التبعيات (Node Packages)

من مجلّد المشروع الرئيسي:

```bash
cd frontend
npm install
```

سيتم تثبيت الحزم التالية (على سبيل المثال):

- `next@14.1.0`
- `react`
- `react-dom`
- `tailwindcss`
- `axios`
- `react-katex`, `katex`
- وغيرها حسب [`package.json`](mualleem-ai-tutor/frontend/package.json:1)

### 4.2 تشغيل خادم التطوير (Development Server)

```bash
cd frontend
npm run dev
```

**العنوان الافتراضي:**

```text
http://localhost:3000
```

### 4.3 بناء نسخة الإنتاج (Production Build)

عند الحاجة لاختبار نسخة Production محلية:

```bash
cd frontend
npm run build
npm start
```

---

## 5. ☁️ إعداد الخدمات السحابية (Qdrant Cloud & Requesty.ai)

### 5.1 إعداد Qdrant Cloud

1. أنشئ حساب على: https://cloud.qdrant.io
2. أنشئ Cluster جديد (مجاني أو مدفوع حسب احتياجك).
3. من صفحة الإعدادات (Settings)، احصل على:
   - **REST URL** – يستخدم كـ `QDRANT_URL`
   - **API Key** – يستخدم كـ `QDRANT_API_KEY`
4. في لوحة Qdrant، أنشئ Collection باسم مثل:
   - `mualleem_curriculum`  
   أو استخدم الاسم الافتراضي المذكور في التوثيق.

أضف هذه القيم إلى ملف `.env` في backend كما في القسم السابق.

تفاصيل إضافية في:  
- [`QDRANT_SETUP_EN.md`](mualleem-ai-tutor/QDRANT_SETUP_EN.md:17)  
- [`README_QDRANT.md`](mualleem-ai-tutor/README_QDRANT.md:1)  

### 5.2 إعداد Requesty.ai

1. أنشئ حساب على: https://app.requesty.ai
2. من لوحة التحكم، أنشئ أو انسخ **API Key**.
3. ثبّت القيم في ملف `.env`:

```env
REQUESTY_API_KEY=your_requesty_api_key_here
REQUESTY_BASE_URL=https://router.requesty.ai/v1
SITE_URL=http://localhost:3000
SITE_NAME=Mualleem - AI Tutoring Platform
```

4. تأكّد من أن الـ Base URL هو بالضبط:
   - `https://router.requesty.ai/v1`

لمزيد من التفاصيل راجع:  
- [`REQUESTY_INTEGRATION.md`](mualleem-ai-tutor/REQUESTY_INTEGRATION.md:1)  
- [`REQUESTY_SETUP_COMPLETE.md`](mualleem-ai-tutor/REQUESTY_SETUP_COMPLETE.md:1)  
- [`REQUESTY_ARABIC.md`](mualleem-ai-tutor/REQUESTY_ARABIC.md:1)

---

## 6. 🔑 ملخّص متغيرات البيئة (Environment Variables Summary)

في ملف `backend/.env`:

```env
# Requesty.ai
REQUESTY_API_KEY=...
REQUESTY_BASE_URL=https://router.requesty.ai/v1
SITE_URL=http://localhost:3000
SITE_NAME=Mualleem - AI Tutoring Platform

# Backend Server
PORT=8000
HOST=0.0.0.0

# Qdrant Cloud
QDRANT_URL=...
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=mualleem_curriculum
```

---

## 7. ✅ خطوات التحقق (Verification Steps)

### 7.1 التحقق من صحة الـ Backend

1. التأكد من أن خادم FastAPI يعمل:

```bash
curl http://localhost:8000/health
```

**متوقّع:**

```json
{
  "status": "healthy",
  "service": "Mualleem Backend"
}
```

2. التحقق من إحصائيات RAG / Qdrant:

```bash
curl http://localhost:8000/stats
```

يجب أن يعرض معلومات عن الـ Collection في Qdrant.

### 7.2 التحقق من رفع منهج (Curriculum Upload)

جرّب رفع ملف PDF (كتجربة):

```bash
curl -X POST http://localhost:8000/upload-curriculum \
  -F "file=@/path/to/textbook.pdf"
```

- إذا نجح، سيتم تقسيم الكتاب إلى مقاطع (Chunks) وتخزينها في Qdrant.
- راجع [`REQUESTY_SETUP_COMPLETE.md`](mualleem-ai-tutor/REQUESTY_SETUP_COMPLETE.md:220) و[`QDRANT_SETUP_EN.md`](mualleem-ai-tutor/QDRANT_SETUP_EN.md:176) لمزيد من الأمثلة.

### 7.3 التحقق من واجهة الدردشة (Chat)

1. تأكّد أن:
   - Backend يعمل على `http://localhost:8000`
   - Frontend يعمل على `http://localhost:3000`
2. افتح المتصفح وانتقل إلى:
   - `http://localhost:3000`
3. جرّب:
   - كتابة سؤال بالعربية مثل:  
     «ما هو قانون فيثاغورس؟»
   - أو رفع صورة لمسألة رياضية.
4. تأكّد من:
   - ظهور الرد بالعربية.
   - عرض المعادلات بـ LaTeX بشكل صحيح (مثل: `x^2 + y^2 = r^2`).

---

## 8. 📌 ملخص سريع (Quick Recap)

1. تثبيت المتطلبات (Python 3.11+, Node 18+).
2. إنشاء بيئة افتراضية في `backend/` وتثبيت `requirements.txt`.
3. إنشاء ملف `.env` في `backend/` بإعدادات:
   - Requesty.ai (API Key + Base URL + SITE_URL + SITE_NAME)
   - Qdrant Cloud (URL + API Key + Collection Name)
4. اختبار:
   - `python3 test_qdrant.py`
   - `python3 test_requesty.py`
5. تشغيل Backend:
   - `python3 main.py`
6. تثبيت تبعيات الـ Frontend وتشغيله:
   - `cd frontend && npm install && npm run dev`
7. التحقق من `/health` و`/stats` واختبار الرفع والدردشة.

---

**بهذه الخطوات تكون منصة «معلّم» جاهزة للعمل في بيئة التطوير مع تكامل كامل مع Qdrant Cloud وRequesty.ai.**  