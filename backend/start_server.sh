#!/usr/bin/env bash
set -euo pipefail

# Mualleem Backend Server Startup Script
#
# Usage:
#   ./start_server.sh
#
# Behavior:
# - Ensures .env exists
# - Ensures data directory exists
# - Ensures dependencies are installed in backend/.venv (if present) or system Python
# - Runs core RAG tests (non-fatal on failure)
# - Starts Uvicorn with autoreload

echo "🚀 Starting Mualleem Backend Server..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null 2>&1 && pwd)"
cd "${SCRIPT_DIR}"

# Check if .env file exists
if [[ ! -f .env ]]; then
    echo "⚠️  Warning: backend/.env file not found!"
    echo "Please create backend/.env with the required Requesty/Qdrant configuration."
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p data

# Recreate virtualenv to ensure it's not corrupted
VENV_DIR="${SCRIPT_DIR}/.venv"
if [[ -d "${VENV_DIR}" ]]; then
    echo "🗑️ Removing existing virtualenv..."
    rm -rf "${VENV_DIR}"
fi

echo "🐍 Creating new virtualenv..."
python3 -m venv "${VENV_DIR}"
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"
echo ""

# Ensure pip is available
if ! python3 -m pip --version &>/dev/null 2>&1; then
    echo "🐍 pip not found. Installing/upgrading pip..."
    python3 -m ensurepip --upgrade
    echo ""
fi

# Ensure dependencies are installed
if ! python3 -c "import fastapi" &>/dev/null 2>&1; then
    echo "📦 Installing backend dependencies from requirements.txt..."
    python3 -m pip install -r requirements.txt
    echo ""
fi

# Run the RAG tests (non-fatal if they fail, but warn)
if [[ -f test_rag.py ]]; then
    echo "🧪 Running RAG service tests (non-blocking)..."
    if ! python3 test_rag.py; then
        echo "⚠️  Warning: test_rag.py reported issues. Check output above."
    fi
    echo ""
fi

# Start the server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "📖 ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
