#!/bin/bash

# Mualleem Backend Server Startup Script

echo "🚀 Starting Mualleem Backend Server..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env file with your OPENAI_API_KEY"
    exit 1
fi

# Check if OpenAI API key is set
if grep -q "your_openai_api_key_here" .env; then
    echo "⚠️  Warning: Please set your actual OPENAI_API_KEY in .env file"
    echo ""
fi

# Check if dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    python3 -m pip install -r requirements.txt --user
    echo ""
fi

# Create data directory if it doesn't exist
mkdir -p data

# Run the test suite first
echo "🧪 Running RAG service tests..."
python3 test_rag.py
echo ""

# Start the server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "📖 ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
