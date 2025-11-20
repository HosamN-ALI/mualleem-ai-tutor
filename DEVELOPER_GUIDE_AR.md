# 🧑‍💻 دليل إعداد المطوّر (Developer Guide) لمنصة معلّم

> هذا الدليل موجّه للمطوّرين الذين يعملون على مشروع **Mualleem AI Tutor** ويحتاجون لفهم طريقة تشغيل بيئة التطوير، وأساليب الاختبار، وخط سير العمل، وحل المشاكل الشائعة.

---

## 1. 🏗 لمحة سريعة عن هيكل المشروع

المشروع مقسوم إلى **Backend** و **Frontend** مع مجموعة من ملفات التوثيق:

```text
mualleem-ai-tutor/
├── backend/                 # خادم FastAPI + RAG + Qdrant + Requesty.ai
│   ├── main.py             # نقطة الدخول الرئيسية (FastAPI app)
│   ├── rag_service.py      # منطق RAG (رفع مناهج + بحث + استرجاع)
│   ├── rag_engine.py       # التكامل مع Qdrant + Requesty.ai
│   ├── test_qdrant.py      # اختبار اتصال Qdrant
│   ├── test_requesty.py    # اختبار تكامل Requesty.ai
│   ├── test_rag.py         # اختبارات RAG (إن وجدت)
│   ├── requirements.txt    # تبعيات Python
│   └── .env                # متغيرات البيئة (محلياً فقط)
│
├── frontend/               # تطبيق Next.js (واجهة الدردشة)
│   ├── app/               # App Router
│   ├── components/        # مكونات ChatInterface وChatBubble
│   ├── package.json       # تبعيات Node + سكربتات التشغيل
│   └── ... ملفات config   # Tailwind, TS, Next
│
├── *.md                    # توثيق Qdrant + Requesty + ملخصات
└── INSTALLATION_GUIDE_AR.md / DEVELOPER_GUIDE_AR.md / OPERATIONAL_GUIDE_AR.md
```

---

## 2. ▶️ تشغيل خوادم التطوير (Development Servers)

### 2.1 Backend (FastAPI + Uvicorn)

#### 2.1.1 المتطلبات

- Python 3.11+
- تفعيل البيئة الافتراضية `.venv`
- ملف `.env` مهيأ كما في دليل التثبيت [`INSTALLATION_GUIDE_AR.md`](mualleem-ai-tutor/INSTALLATION_GUIDE_AR.md:1)

#### 2.1.2 تفعيل البيئة وتثبيت التبعيات

```bash
cd mualleem-ai-tutor/backend

# إنشاء بيئة افتراضية إن لم تكن موجودة
python3 -m venv .venv

# تفعيل البيئة (Linux/macOS)
source .venv/bin/activate

# تثبيت التبعيات
pip install -r requirements.txt
```

#### 2.1.3 تشغيل الخادم

أبسط طريقة (حسب التوثيق الداخلي):

```bash
cd backend
python3 main.py
```

أو باستخدام `uvicorn` بشكل مباشر:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- الخادم سيكون على: `http://localhost:8000`
- Endpoint صحيحة للتأكد: `GET /health`

---

### 2.2 Frontend (Next.js 14 + App Router)

#### 2.2.1 تثبيت التبعيات

```bash
cd mualleem-ai-tutor/frontend
npm install
```

#### 2.2.2 تشغيل خادم التطوير

```bash
cd frontend
npm run dev
```

- عنوان الواجهة: `http://localhost:3000`

#### 2.2.3 بناء نسخة الإنتاج للتجربة المحلية

```bash
cd frontend
npm run build
npm start
```

---

## 3. 🧪 إجراءات الاختبار (Testing Procedures)

### 3.1 اختبارات الـ Backend

#### 3.1.1 اختبار اتصال Qdrant Cloud

الملف: [`backend/test_qdrant.py`](mualleem-ai-tutor/backend/test_qdrant.py:1)

التشغيل:

```bash
cd backend
source .venv/bin/activate
python3 test_qdrant.py
```

متوقّع:

```text
✅ Successfully connected to Qdrant Cloud!
✅ Collection 'curriculum_collection' (أو mualleem_curriculum) موجودة
✅ All tests passed!
```

إذا ظهرت أخطاء، راجع:
- [`QDRANT_SETUP_EN.md`](mualleem-ai-tutor/QDRANT_SETUP_EN.md:1)
- [`QDRANT_QUICKSTART.md`](mualleem-ai-tutor/QDRANT_QUICKSTART.md:1)
- [`SUMMARY_AR.md`](mualleem-ai-tutor/SUMMARY_AR.md:1)

#### 3.1.2 اختبار تكامل Requesty.ai

الملف: [`backend/test_requesty.py`](mualleem-ai-tutor/backend/test_requesty.py:1)

التشغيل:

```bash
cd backend
source .venv/bin/activate
python3 test_requesty.py
```

متوقّع (كما في [`REQUESTY_SETUP_COMPLETE.md`](mualleem-ai-tutor/REQUESTY_SETUP_COMPLETE.md:38)):

- نجاح اختبار الـ API Key
- نجاح Chat Completion باستخدام `openai/gpt-4o-mini`
- نجاح Embeddings باستخدام `openai/text-embedding-3-small`

#### 3.1.3 اختبارات RAG (إن وُجدت)

الملف: [`backend/test_rag.py`](mualleem-ai-tutor/backend/test_rag.py:1)

تشغيل:

```bash
cd backend
source .venv/bin/activate
python3 test_rag.py
```

هذه الاختبارات عادةً تتحقق من:
- تحميل PDF واستخراج النص
- إنشاء Chunks
- تخزينها في Qdrant
- أداء بحث دلالي (Semantic Search)

---

### 3.2 اختبارات الـ Frontend

مذكورة في [`FRONTEND_COMPLETE.md`](mualleem-ai-tutor/FRONTEND_COMPLETE.md:130):

#### 3.2.1 TypeScript و build

```bash
cd frontend

# فحص TypeScript (يتم ضمن build غالباً)
npm run build
```

متوقّع:
- لا توجد أخطاء TypeScript
- Production build ناجح

#### 3.2.2 تشغيل خادم التطوير واختباره

```bash
cd frontend
npm run dev
```

ثم افتح المتصفح على `http://localhost:3000` وتحقّق من:
- تحميل الصفحة بدون أخطاء
- مكوّن الدردشة يعمل
- رفع الصور يعمل
- LaTeX يظهر بشكل صحيح

---

## 4. 🧰 خطوات العمل اليومية (Development Workflow)

### 4.1 دورة العمل النموذجية Backend

1. تفعيل البيئة الافتراضية:

   ```bash
   cd backend
   source .venv/bin/activate
   ```

2. سحب آخر التغييرات من git (إن وجدت).

3. تعديل الأكواد في الملفات الرئيسة:
   - [`main.py`](mualleem-ai-tutor/backend/main.py:1) – تعريف الـ FastAPI endpoints.
   - [`rag_service.py`](mualleem-ai-tutor/backend/rag_service.py:1) – عمليات RAG (رفع PDF، الفهرسة، الاسترجاع).
   - [`rag_engine.py`](mualleem-ai-tutor/backend/rag_engine.py:13) – التكامل مع Qdrant Cloud وRequesty.ai.

4. تشغيل الخادم في وضع التطوير:

   ```bash
   uvicorn main:app --reload
   ```

5. اختبار Endpoints يدويًا عبر:
   - `curl`
   - أو متصفح / أدوات مثل Postman / Thunder Client

### 4.2 دورة العمل النموذجية Frontend

1. من مجلّد `frontend`:

   ```bash
   npm run dev
   ```

2. تطوير واجهة الدردشة في:
   - [`components/ChatInterface.tsx`](mualleem-ai-tutor/frontend/components/ChatInterface.tsx:1)
   - [`components/ChatBubble.tsx`](mualleem-ai-tutor/frontend/components/ChatBubble.tsx:1)
   - [`app/page.tsx`](mualleem-ai-tutor/frontend/app/page.tsx:1)

3. التأكد من أن استدعاءات API تتجه إلى:
   - `POST http://localhost:8000/chat`
   - `POST http://localhost:8000/upload-curriculum` (للاستخدام التشغيلي/التجريبي)

4. اختبار التعديلات مباشرة عبر المتصفح مع **Hot Reloading**.

---

## 5. 🐛 الأعطال الشائعة (Common Troubleshooting)

### 5.1 مشاكل Backend

#### 5.1.1 خطأ: `REQUESTY_API_KEY not set` أو `Invalid API Key`

- تأكّد من:
  - وجود `REQUESTY_API_KEY` في `backend/.env`
  - أن القيمة صحيحة ومأخوذة من لوحة `app.requesty.ai`
  - تفعيل البيئة قبل التشغيل حتى يتم تحميل `.env`
- راجع قسم Troubleshooting في [`REQUESTY_SETUP_COMPLETE.md`](mualleem-ai-tutor/REQUESTY_SETUP_COMPLETE.md:194)

#### 5.1.2 خطأ: `Cannot connect to Qdrant` أو `Connection Timeout`

- تأكّد من:
  - `QDRANT_URL` صحيح ويحتوي على البروتوكول والمنفذ، مثل:  
    `https://....qdrant.io:6333`
  - `QDRANT_API_KEY` صحيح.
- شغّل:

  ```bash
  cd backend
  source .venv/bin/activate
  python3 test_qdrant.py
  ```

- راجع [`QDRANT_SETUP_EN.md`](mualleem-ai-tutor/QDRANT_SETUP_EN.md:219) لقسم Troubleshooting.

#### 5.1.3 خطأ: `Collection not found`

- في معظم الحالات، يقوم الكود بإنشاء الـ Collection إذا لم تكن موجودة.
- يمكنك تشغيل سكربت يقوم بتهيئة RAG، أو الاعتماد على `rag_service` عند رفع أول PDF.
- تحقق من المنطق داخل [`rag_service.py`](mualleem-ai-tutor/backend/rag_service.py:1).

#### 5.1.4 خطأ: `Module not found` أو ImportError

- غالباً سببه:
  - عدم تثبيت التبعيات بشكل صحيح.
  - نسيان تفعيل البيئة الافتراضية.
- الحل:

  ```bash
  cd backend
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

---

### 5.2 مشاكل Frontend

#### 5.2.1 أخطاء TypeScript أو Build

- راجع الرسائل في `npm run build`
- عدّل أنواع المتغيّرات أو الاستيرادات في الملفات المذكورة في الخطأ.
- تأكّد من وجود ملفات React/TSX المشار إليها وعدم تغيير مساراتها.

#### 5.2.2 فشل الاتصال بالـ Backend (CORS / Network)

- تأكّد من أن:
  - Backend يعمل على `http://localhost:8000`
  - الـ URL في جانب الـ Frontend (غالباً في `ChatInterface.tsx`) موجّه إلى نفس العنوان.
- إذا كانت هناك مشاكل CORS:
  - تأكّد من إعداد `CORSMiddleware` في `main.py` (إن وجد).
  - تأكّد من أن `origins` تشمل `http://localhost:3000`.

---

## 6. 🔁 سيناريوهات عمل مطوّر (End-to-End Dev Scenarios)

### 6.1 سيناريو: إضافة تحسين في واجهة الدردشة

1. شغّل Backend:

   ```bash
   cd backend
   source .venv/bin/activate
   python3 main.py
   ```

2. شغّل Frontend:

   ```bash
   cd frontend
   npm run dev
   ```

3. عدّل في:
   - واجهة المستخدم: [`ChatInterface.tsx`](mualleem-ai-tutor/frontend/components/ChatInterface.tsx:1)
   - شكل الفقاعات: [`ChatBubble.tsx`](mualleem-ai-tutor/frontend/components/ChatBubble.tsx:1)

4. جرب إرسال أسئلة وصور، وتحقق من:
   - البيانات المرسلة من الـ Frontend إلى `/chat`
   - بنية الـ response في الـ Backend

### 6.2 سيناريو: تعديل منطق RAG أو طريقة تقسيم المناهج

1. عدّل في [`rag_service.py`](mualleem-ai-tutor/backend/rag_service.py:1) أو [`rag_engine.py`](mualleem-ai-tutor/backend/rag_engine.py:13).
2. شغّل اختبارات:
   - `python3 test_qdrant.py`
   - `python3 test_rag.py` (إن وجد)
3. شغّل الخادم ثم ارفع PDF تجريبي:
   - راجع دليل التشغيل [`OPERATIONAL_GUIDE_AR.md`](mualleem-ai-tutor/OPERATIONAL_GUIDE_AR.md:1) (بعد إنشائه).

---

## 7. 📚 مراجع للمطوّر داخل المشروع

- دليل التثبيت الكامل: [`INSTALLATION_GUIDE_AR.md`](mualleem-ai-tutor/INSTALLATION_GUIDE_AR.md:1)
- ملخّص إعداد Qdrant: [`QDRANT_SETUP_EN.md`](mualleem-ai-tutor/QDRANT_SETUP_EN.md:1)
- دليل Qdrant بالعربية: [`README_QDRANT.md`](mualleem-ai-tutor/README_QDRANT.md:1)
- تكامل Requesty.ai بالعربية: [`REQUESTY_ARABIC.md`](mualleem-ai-tutor/REQUESTY_ARABIC.md:1)
- ملخّص تكامل Requesty: [`REQUESTY_SETUP_COMPLETE.md`](mualleem-ai-tutor/REQUESTY_SETUP_COMPLETE.md:1)
- ملخّص الواجهة الأمامية: [`FRONTEND_COMPLETE.md`](mualleem-ai-tutor/FRONTEND_COMPLETE.md:1)
- نظرة معمارية شاملة: [`ARCHITECTURE.md`](mualleem-ai-tutor/ARCHITECTURE.md:1)
- فهرس التوثيق: [`DOCUMENTATION_INDEX.md`](mualleem-ai-tutor/DOCUMENTATION_INDEX.md:1)

---

## 8. 🏁 خاتمة

هذا الدليل يهدف لتسهيل عمل المطوّر على منصة «معلّم» من خلال:

- توحيد طريقة تشغيل خوادم التطوير.
- توثيق خطوات الاختبار الأساسيّة.
- جمع حلول المشاكل الشائعة في مكان واحد.
- توضيح خط سير العمل القياسي بين Backend وFrontend.

باستخدام هذا الدليل مع بقية ملفات التوثيق في المشروع، يمكن لأي مطوّر جديد الانضمام بسرعة والعمل بثقة على تحسين المنصة.  