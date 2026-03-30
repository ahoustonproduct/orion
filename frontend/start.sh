#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"

echo "=== Orion Code — WashU FinTech Edition ==="
echo ""

# 1. Check for ANTHROPIC_API_KEY
if [ -f "$BACKEND_DIR/.env" ]; then
  export $(grep -v '^#' "$BACKEND_DIR/.env" | xargs)
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "⚠️  No ANTHROPIC_API_KEY found."
  echo "   Create $BACKEND_DIR/.env with:"
  echo "   ANTHROPIC_API_KEY=your_key_here"
  echo ""
fi

# 2. Install backend dependencies if needed
cd "$BACKEND_DIR"
if ! python3 -c "import fastapi" 2>/dev/null; then
  echo "📦 Installing backend dependencies..."
  pip3 install -r requirements.txt --quiet
fi

# 3. Generate datasets if not already done
DATASETS_DIR="$BACKEND_DIR/datasets"
if [ ! -f "$DATASETS_DIR/loan_applications.csv" ]; then
  echo "📊 Generating datasets (first run only)..."
  cd "$DATASETS_DIR"
  python3 seed.py
  cd "$BACKEND_DIR"
fi

# 4. Start backend
echo "🚀 Starting backend on http://localhost:8000 ..."
uvicorn main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready
sleep 2

# 5. Start frontend
cd "$PROJECT_DIR"
echo ""
echo "🌐 Starting frontend on http://localhost:3000 ..."
echo ""
npm run dev &
FRONTEND_PID=$!

echo "=== App running ==="
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers."

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'" EXIT
wait
