#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/../backend"

echo "=== Orion Code — WashU FinTech Edition ==="
echo ""

# 1. Start backend (Ollama-ready)
echo "[1/2] Checking Ollama Backend..."

cd "$BACKEND_DIR"
if [ ! -d "venv" ]; then
  echo "  Creating virtual environment..."
  python3 -m venv venv
fi

echo "  Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt --quiet

echo "🚀 Starting backend on http://0.0.0.0:8001 ..."
uvicorn main:app --host 0.0.0.0 --port 8001 --reload &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready
sleep 3

# 2. Start frontend
cd "$PROJECT_DIR"
echo ""
echo "🌐 Starting frontend on http://0.0.0.0:3000 ..."
echo ""
export BACKEND_URL="http://localhost:8001"
npm run dev -- -H 0.0.0.0 &
FRONTEND_PID=$!

echo "=== App running ==="
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop both servers."

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'" EXIT
wait
