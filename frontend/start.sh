#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/../backend"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-3000}"
export ORION_AI_ENABLED="${ORION_AI_ENABLED:-false}"

echo "=== Orion Code: WashU FinTech Edition ==="
echo ""

# 1. Start backend
echo "[1/2] Starting backend..."

cd "$BACKEND_DIR"
if [ ! -d "venv" ]; then
  echo "  Creating virtual environment..."
  python3 -m venv venv
fi

echo "  Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt --quiet

echo "🚀 Starting backend on http://0.0.0.0:${BACKEND_PORT} ..."
uvicorn main:app --host 0.0.0.0 --port "${BACKEND_PORT}" --reload &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready
sleep 3

# 2. Start frontend
cd "$PROJECT_DIR"
echo ""
echo "🌐 Starting frontend on http://0.0.0.0:${FRONTEND_PORT} ..."
echo ""
export BACKEND_URL="${BACKEND_URL:-http://localhost:${BACKEND_PORT}}"
npm run dev -- -H 0.0.0.0 -p "${FRONTEND_PORT}" &
FRONTEND_PID=$!

echo "=== App running ==="
echo "   Frontend: http://localhost:${FRONTEND_PORT}"
echo "   Backend:  http://localhost:${BACKEND_PORT}"
echo "   AI:       optional, ORION_AI_ENABLED=${ORION_AI_ENABLED}"
echo ""
echo "Press Ctrl+C to stop both servers."

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'" EXIT
wait
