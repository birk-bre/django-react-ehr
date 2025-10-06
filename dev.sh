#!/bin/bash

# Patient EHR System - Development Script
# Starts both backend and frontend servers concurrently

set -e

echo "========================================"
echo "Patient EHR System - Development Mode"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "Error: Frontend dependencies not installed!"
    echo "Please run ./setup.sh first"
    exit 1
fi

echo "Starting both backend and frontend servers..."
echo ""
echo "Backend will run on:  http://localhost:8000"
echo "Frontend will run on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""
echo "========================================"
echo ""

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend in background
echo "Starting Django backend..."
source venv/bin/activate
python manage.py runserver 8000 > /tmp/django.log 2>&1 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start frontend in background
echo "Starting React frontend..."
cd frontend
npm run dev > /tmp/vite.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✓ Both servers started successfully!"
echo ""
echo "View logs:"
echo "  Backend:  tail -f /tmp/django.log"
echo "  Frontend: tail -f /tmp/vite.log"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
