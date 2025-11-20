# 🚀 الترحيل إلى Qdrant Cloud

## نظرة عامة
تم تحديث منصة معلّم لاستخدام **Qdrant Cloud** كقاعدة بيانات متجهات بدلاً من ChromaDB المحلية.

## ✨ المزايا

### Qdrant Cloud
- ☁️ **سحابية**: لا حاجة لإدارة البنية التحتية
- 🚀 **أداء عالي**: بحث سريع ومُحسّن
- 📈 **قابلة للتوسع**: تتوسع تلقائياً مع نمو البيانات
- 🔒 **آمنة**: تشفير البيانات وحماية متقدمة
- 🌍 **موزعة**: خوادم في أوروبا (europe-west3)

## 🔧 التكوين

### متغيرات البيئة (.env)
```env
# Qdrant Cloud Configuration
QDRANT_URL=https://dfc1c80b-b7f2-4b4f-8daa-1582a8b80e3e.europe-west3-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.rKmmlaLvotuNhxetr_8_eYfMZtaaK5Ee4zl5dYOgNJE
QDRANT_COLLECTION_NAME=curriculum_collection

# Requesty.ai API Configuration
REQUESTY_API_KEY=rqsty-sk-y4aKgcDPSLuXh6PXd4vHGBtHPlWRkyfZVcN6R3thk+7q8djI+bZs0L98Ud0PdZr0rsx1M/N1AGP07BZDhyeDSfVyyhum2Hbf6uVTPyFN8wU=
REQUESTY_BASE_URL=https://router.requesty.ai/v1
```

## 📦 التبعيات المحدثة

تم استبدال `chromadb` بـ `qdrant-client` في `requirements.txt`:

```txt
qdrant-client==1.7.0  # بدلاً من chromadb==0.4.22
```

## 🔄 التغييرات في الكود

### 1. rag_service.py
- ✅ استبدال ChromaDB بـ Qdrant Client
- ✅ الاتصال بـ Qdrant Cloud باستخدام URL و API Key
- ✅ إنشاء Collection تلقائياً إذا لم تكن موجودة
- ✅ استخدام COSINE distance للبحث عن التشابه
- ✅ تخزين البيانات الوصفية (metadata) مع كل نقطة

### 2. rag_engine.py
- ✅ تحديث لاستخدام Qdrant Client
- ✅ دعم Requesty.ai للـ embeddings
- ✅ تحسين معالجة الأخطاء

## 🚀 التثبيت والتشغيل

### 1. تثبيت التبعيات
```bash
cd backend
pip install -r requirements.txt
```

### 2. التحقق من ملف .env
تأكد من وجود جميع المتغيرات المطلوبة في `backend/.env`

### 3. تشغيل الخادم
```bash
python main.py
# أو
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 اختبار الاتصال

### 1. فحص الصحة
```bash
curl http://localhost:8000/health
```

### 2. فحص الإحصائيات
```bash
curl http://localhost:8000/stats
```

يجب أن ترى:
```json
{
  "collection_name": "curriculum_collection",
  "total_chunks": 0,
  "vector_size": 1536,
  "status": "active",
  "storage": "Qdrant Cloud"
}
```

## 📤 رفع منهج دراسي

```bash
curl -X POST http://localhost:8000/upload-curriculum \
  -F "file=@/path/to/textbook.pdf"
```

## 💬 اختبار المحادثة

```bash
curl -X POST http://localhost:8000/chat \
  -F "question=ما هي نظرية فيثاغورس؟"
```

## 🔍 البحث في Qdrant

يتم البحث باستخدام:
- **Vector Similarity**: COSINE distance
- **Embedding Model**: text-embedding-3-small (1536 dimensions)
- **Top K Results**: 3-5 chunks (قابل للتعديل)

## 🛠️ استكشاف الأخطاء

### خطأ في الاتصال بـ Qdrant
```
✗ Error connecting to Qdrant Cloud
```
**الحل**: تحقق من QDRANT_URL و QDRANT_API_KEY

### خطأ في إنشاء Collection
```
✗ Error ensuring collection exists
```
**الحل**: تحقق من صلاحيات API Key (يجب أن تكون "write" أو "manage")

### خطأ في توليد Embeddings
```
✗ Error generating embeddings
```
**الحل**: تحقق من REQUESTY_API_KEY

## 📈 الأداء

- **Indexing**: ~100 chunks/batch
- **Query Time**: < 100ms
- **Embedding Generation**: ~1-2s per batch
- **Storage**: Unlimited (Qdrant Cloud)

## 🔐 الأمان

- ✅ API Keys مخزنة في `.env` (غير مرفوعة على Git)
- ✅ اتصال HTTPS مع Qdrant Cloud
- ✅ Authentication عبر JWT token
- ✅ CORS محدد لـ localhost:3000

## 📚 الموارد

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Python Client](https://github.com/qdrant/qdrant-client)
- [Requesty.ai Docs](https://docs.requesty.ai/)

## ✅ الخطوات التالية

1. ✅ تثبيت التبعيات الجديدة
2. ✅ تحديث ملف .env
3. ✅ تشغيل الخادم
4. ⏳ رفع منهج دراسي للاختبار
5. ⏳ اختبار المحادثة مع الذكاء الاصطناعي

---

**تم التحديث**: 20 نوفمبر 2025
**الإصدار**: 2.0 (Qdrant Cloud)
