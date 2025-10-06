#!/bin/bash

# Patient EHR System - Frontend Server Script
# Starts the React development server with Vite

set -e

echo "Starting React frontend server..."
echo ""

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "Error: node_modules not found!"
    echo "Please run ./setup.sh first or run 'npm install' in the frontend directory"
    exit 1
fi

cd frontend

echo "========================================"
echo "React Frontend Server (Vite)"
echo "========================================"
echo "Server: http://localhost:3000"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the development server
npm run dev
