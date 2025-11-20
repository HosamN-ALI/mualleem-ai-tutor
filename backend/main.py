from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from rag_service import rag_service, get_openai_client, SYSTEM_PROMPT
from collections import defaultdict
import time
import logging
from performance_monitor import perf_monitor, monitor_endpoint
from typing import Optional
from pydantic import BaseModel, Field
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="Mualleem API", version="1.0.0")

# Initialize Supabase client
supabase_url = os.getenv("VITE_SUPABASE_URL")
supabase_key = os.getenv("VITE_SUPABASE_SUPABASE_ANON_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Image upload configuration
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Simple rate limiting - temporary for development
request_counts = defaultdict(list)
RATE_LIMIT = 60  # requests per minute
RATE_WINDOW = 60  # seconds

# Ensure data directory exists
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        # Public IP access (external browsers)
        "http://216.81.248.146:3000",
        "http://216.81.248.146:3001",
        "http://216.81.248.146:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_image_file(file: UploadFile):
    """
    Validate image file type and size
    
    Args:
        file: Uploaded file to validate
        
    Raises:
        HTTPException: With appropriate status codes for validation errors
    """
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="اسم الملف مفقود"
        )
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="نوع الملف غير مدعوم. يرجى استخدام PNG, JPG, GIF, أو WEBP"
        )
    
    # Check file size by reading content
    try:
        file_content = file.file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="حجم الملف كبير جداً. الحد الأقصى 10 ميجابايت"
            )
        
        # Reset file pointer for later processing
        file.file.seek(0)
        return True
        
    except Exception as e:
        logger.error(f"Error validating file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail="خطأ في قراءة الملف. يرجى التأكد من صحة الملف"
        )

def check_rate_limit(request: Request):
    """
    Simple rate limiting check
    
    Args:
        request: FastAPI request object
        
    Raises:
        HTTPException: If rate limit is exceeded
    """
    client_ip = request.client.host
    now = time.time()
    
    # Clean old requests
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip]
        if now - req_time < RATE_WINDOW
    ]
    
    if len(request_counts[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="تم تجاوز عدد الطلبات المسموح. يرجى المحاولة لاحقاً"
        )
    
    request_counts[client_ip].append(now)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler for better error reporting"""
    logger.error(f"خطأ غير متوقع: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "حدث خطأ في الخادم. يرجى المحاولة لاحقاً"}
    )

@app.get("/")
async def root():
    return {"message": "مرحباً بك في منصة معلّم التعليمية", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Mualleem Backend"}

@app.get("/stats")
async def get_stats():
    """
    Get statistics about the indexed curriculum
    """
    stats = rag_service.get_collection_stats()
    return stats

@app.post("/upload-curriculum")
@monitor_endpoint("/upload-curriculum")
async def upload_curriculum(file: UploadFile = File(...)):
    """
    Upload and index a PDF textbook for RAG
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="يجب أن يكون الملف بصيغة PDF")
    
    try:
        start_time = time.time()
        perf_monitor.log_system_resources()
        
        # Save uploaded file
        file_path = DATA_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_save_time = time.time()
        logger.info(f"PERFORMANCE: File save took {file_save_time - start_time:.3f}s")
        
        # Index the PDF using RAG service
        result = rag_service.index_pdf(str(file_path), document_name=file.filename)
        
        total_time = time.time()
        logger.info(f"PERFORMANCE: PDF indexing took {total_time - file_save_time:.3f}s")
        logger.info(f"PERFORMANCE: Total upload+index took {total_time - start_time:.3f}s")
        
        return {
            "message": "تم رفع المنهج وفهرسته بنجاح",
            "filename": file.filename,
            "total_chunks": result["total_chunks"],
            "total_characters": result["total_characters"],
            "status": "indexed",
            "processing_time_seconds": round(total_time - start_time, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في معالجة الملف: {str(e)}")

@app.post("/chat")
@monitor_endpoint("/chat")
async def chat(
    request: Request,
    question: str = Form(...),
    image: Optional[UploadFile] = File(None),
):
    """
    Chat endpoint: accepts text question and optional image
    Returns AI response with step-by-step explanation in Arabic
    """
    overall_start = time.time()
    perf_monitor.log_system_resources()
    
    # Check rate limit
    check_rate_limit(request)
    
    if not question and not image:
        raise HTTPException(status_code=400, detail="يجب إرسال سؤال أو صورة")
    
    # Validate image if provided
    if image:
        validate_image_file(image)
    
    try:
        # Step 1: Query Qdrant for relevant context
        rag_start = time.time()
        rag_results = rag_service.query_similar_chunks(question, n_results=3)
        context_text = "\n\n".join([chunk["text"] for chunk in rag_results["context_chunks"]])
        rag_end = time.time()
        logger.info(f"PERFORMANCE: Qdrant query took {rag_end - rag_start:.3f}s")
        
        # Step 2: Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        
        # Add context from curriculum if available
        if context_text:
            context_message = f"**السياق من المنهج الدراسي:**\n\n{context_text}\n\n---\n\n"
            messages.append({"role": "system", "content": context_message})
        
        # Step 3: Handle image if provided
        image_processing_time = 0
        if image:
            image_start = time.time()
            try:
                # Save image temporarily
                image_path = DATA_DIR / f"temp_{image.filename}"
                with open(image_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                
                # Read image as base64
                import base64
                with open(image_path, "rb") as img_file:
                    image_data = base64.b64encode(img_file.read()).decode('utf-8')
                
                # Determine image type
                image_type = "image/jpeg" if image.filename.lower().endswith(('.jpg', '.jpeg')) else "image/png"
                
                image_processing_time = time.time() - image_start
                logger.info(f"PERFORMANCE: Image processing took {image_processing_time:.3f}s")
                
            except Exception as e:
                logger.error(f"Error processing image {image.filename}: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="خطأ في معالجة الصورة. يرجى المحاولة مرة أخرى"
                )
            
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{image_type};base64,{image_data}"
                        }
                    }
                ]
            })
            
            # Clean up temp file
            try:
                os.remove(image_path)
            except:
                pass  # Ignore cleanup errors
        else:
            messages.append({"role": "user", "content": question})
        
        # Step 4: Call OpenAI API via Requesty.ai
        requesty_start = time.time()
        client = get_openai_client()
        response = client.chat.completions.create(
            model="openai/gpt-4o" if image else "openai/gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        requesty_end = time.time()
        requesty_time = requesty_end - requesty_start
        logger.info(f"PERFORMANCE: Requesty API call took {requesty_time:.3f}s")
        
        answer = response.choices[0].message.content
        
        total_time = time.time() - overall_start
        logger.info(f"PERFORMANCE: Total chat request took {total_time:.3f}s")
        
        return {
            "answer": answer,
            "question": question,
            "has_image": image is not None,
            "context_used": len(rag_results["context_chunks"]) > 0,
            "model_used": "openai/gpt-4o" if image else "openai/gpt-4o-mini",
            "provider": "Requesty.ai Gateway",
            "performance_metrics": {
                "total_time": round(total_time, 3),
                "qdrant_query_time": round(rag_end - rag_start, 3),
                "requesty_api_time": round(requesty_time, 3),
                "image_processing_time": round(image_processing_time, 3)
            }
        }
        
    except HTTPException:
        # Re-raise HTTPExceptions (already have proper status codes)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="خطأ في معالجة السؤال. يرجى المحاولة مرة أخرى")

class ReviewSubmission(BaseModel):
    session_id: str = Field(..., description="Client-side session identifier")
    question: str = Field(..., description="Original question asked")
    answer: str = Field(..., description="AI-generated answer")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5 stars")
    feedback: Optional[str] = Field(None, description="Optional text feedback")
    model_used: Optional[str] = Field(None, description="AI model used")
    context_used: bool = Field(False, description="Whether curriculum context was used")
    user_id: Optional[str] = Field(None, description="Optional user ID for authenticated users")

class ReviewResponse(BaseModel):
    id: str
    rating: int
    feedback: Optional[str]
    created_at: str
    message: str

@app.post("/reviews", response_model=ReviewResponse)
async def submit_review(review: ReviewSubmission):
    """
    Submit a review and rating for an AI response
    Allows both anonymous and authenticated users to provide feedback
    """
    try:
        # Prepare review data
        review_data = {
            "session_id": review.session_id,
            "question": review.question,
            "answer": review.answer,
            "rating": review.rating,
            "feedback": review.feedback,
            "model_used": review.model_used,
            "context_used": review.context_used,
            "user_id": review.user_id
        }

        # Insert into Supabase
        result = supabase.table("reviews").insert(review_data).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="فشل في حفظ التقييم")

        review_record = result.data[0]

        return ReviewResponse(
            id=review_record["id"],
            rating=review_record["rating"],
            feedback=review_record.get("feedback"),
            created_at=review_record["created_at"],
            message="تم إرسال التقييم بنجاح. شكراً لملاحظاتك!"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting review: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطأ في إرسال التقييم: {str(e)}")

@app.get("/reviews/stats")
async def get_review_stats():
    """
    Get aggregated statistics about reviews
    Returns total reviews, average rating, and rating distribution
    """
    try:
        # Get all reviews
        result = supabase.table("reviews").select("rating").execute()

        if not result.data:
            return {
                "total_reviews": 0,
                "average_rating": 0,
                "rating_distribution": {str(i): 0 for i in range(1, 6)}
            }

        reviews = result.data
        total_reviews = len(reviews)

        # Calculate average rating
        total_rating = sum(r["rating"] for r in reviews)
        average_rating = round(total_rating / total_reviews, 2) if total_reviews > 0 else 0

        # Calculate rating distribution
        rating_distribution = {str(i): 0 for i in range(1, 6)}
        for review in reviews:
            rating_str = str(review["rating"])
            rating_distribution[rating_str] += 1

        return {
            "total_reviews": total_reviews,
            "average_rating": average_rating,
            "rating_distribution": rating_distribution
        }

    except Exception as e:
        logger.error(f"Error fetching review stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطأ في جلب إحصائيات التقييمات: {str(e)}")

@app.get("/reviews/recent")
async def get_recent_reviews(limit: int = 10):
    """
    Get recent reviews with feedback
    Returns the most recent reviews that include text feedback
    """
    try:
        result = supabase.table("reviews") \
            .select("id, rating, feedback, created_at, model_used") \
            .not_.is_("feedback", "null") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()

        return {
            "reviews": result.data,
            "count": len(result.data)
        }

    except Exception as e:
        logger.error(f"Error fetching recent reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطأ في جلب التقييمات الأخيرة: {str(e)}")

@app.on_event("shutdown")
async def save_performance_report():
    """Save performance report on shutdown"""
    try:
        perf_monitor.save_report("performance_report.json")
        logger.info("Performance report saved successfully")
    except Exception as e:
        logger.error(f"Failed to save performance report: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
