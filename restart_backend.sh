#!/bin/bash

echo "🔄 Restarting Backend Server..."

# Kill any existing backend processes
echo "🛑 Stopping existing backend processes..."
pkill -f "uvicorn main:app" || true

# Wait a moment
sleep 2

# Start the backend
echo "🚀 Starting backend server..."
cd app
source ../venv/bin/activate
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload &

echo "✅ Backend server restarted on http://127.0.0.1:8000"
echo "📊 Health check: http://127.0.0.1:8000/health"
echo "📖 API docs: http://127.0.0.1:8000/docs"
