#!/bin/bash

# Patient EHR System - Backend Server Script
# Starts the Django development server

set -e

echo "Starting Django backend server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if migrations are needed
echo "Checking for pending migrations..."
if python manage.py makemigrations --dry-run --check > /dev/null 2>&1; then
    echo "✓ No pending migrations"
else
    echo "⚠ Pending migrations detected. Running migrations..."
    python manage.py migrate
fi

echo ""
echo "========================================"
echo "Django Backend Server"
echo "========================================"
echo "Server: http://localhost:8000"
echo "API: http://localhost:8000/api/"
echo "Admin: http://localhost:8000/admin/"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the development server
python manage.py runserver 8000
