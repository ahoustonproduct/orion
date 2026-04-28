#!/bin/bash
cd "$(dirname "$0")"

echo "[1/2] Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

echo "  Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt --quiet

export BACKEND_PORT="${BACKEND_PORT:-8000}"
export ORION_AI_ENABLED="${ORION_AI_ENABLED:-false}"

echo "[2/2] Starting backend on port ${BACKEND_PORT}..."
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi
exec uvicorn main:app --reload --host 0.0.0.0 --port "${BACKEND_PORT}"
