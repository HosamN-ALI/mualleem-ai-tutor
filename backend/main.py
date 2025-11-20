from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from rag_service import rag_service, get_openai_client, SYSTEM_PROMPT

load_dotenv()

app = FastAPI(title="Mualleem API", version="1.0.0")

# Ensure data directory exists
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def upload_curriculum(file: UploadFile = File(...)):
    """
    Upload and index a PDF textbook for RAG
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="يجب أن يكون الملف بصيغة PDF")
    
    try:
        # Save uploaded file
        file_path = DATA_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Index the PDF using RAG service
        result = rag_service.index_pdf(str(file_path), document_name=file.filename)
        
        return {
            "message": "تم رفع المنهج وفهرسته بنجاح",
            "filename": file.filename,
            "total_chunks": result["total_chunks"],
            "total_characters": result["total_characters"],
            "status": "indexed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في معالجة الملف: {str(e)}")

@app.post("/chat")
async def chat(
    question: str = Form(...),
    image: UploadFile = File(None)
):
    """
    Chat endpoint: accepts text question and optional image
    Returns AI response with step-by-step explanation in Arabic
    """
    if not question and not image:
        raise HTTPException(status_code=400, detail="يجب إرسال سؤال أو صورة")
    
    try:
        # Step 1: Query ChromaDB for relevant context
        rag_results = rag_service.query_similar_chunks(question, n_results=3)
        context_text = "\n\n".join([chunk["text"] for chunk in rag_results["context_chunks"]])
        
        # Step 2: Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        
        # Add context from curriculum if available
        if context_text:
            context_message = f"**السياق من المنهج الدراسي:**\n\n{context_text}\n\n---\n\n"
            messages.append({"role": "system", "content": context_message})
        
        # Step 3: Handle image if provided
        if image:
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
            os.remove(image_path)
        else:
            messages.append({"role": "user", "content": question})
        
        # Step 4: Call OpenAI API via Requesty.ai
        client = get_openai_client()
        response = client.chat.completions.create(
            model="openai/gpt-4o" if image else "openai/gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        answer = response.choices[0].message.content
        
        return {
            "answer": answer,
            "question": question,
            "has_image": image is not None,
            "context_used": len(rag_results["context_chunks"]) > 0,
            "model_used": "openai/gpt-4o" if image else "openai/gpt-4o-mini",
            "provider": "Requesty.ai Gateway"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في معالجة السؤال: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
