#!/bin/bash

# Patient EHR System - Setup Script
# This script sets up the complete development environment

set -e  # Exit on error

echo "========================================"
echo "Patient EHR System - Initial Setup"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
echo ""

# Check Node.js installation
echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
echo ""

# Backend Setup
echo "========================================"
echo "Setting up Backend (Django)"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists${NC}"
else
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
if command -v uv &> /dev/null; then
    echo "Using uv for package installation..."
    pip install uv > /dev/null 2>&1
    uv pip install django djangorestframework django-cors-headers python-dateutil
else
    echo "Installing with pip..."
    pip install django djangorestframework django-cors-headers python-dateutil
fi
echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Run migrations
echo "Running database migrations..."
python manage.py migrate
echo -e "${GREEN}✓ Database migrations completed${NC}"
echo ""

# Ask to create superuser
echo -e "${YELLOW}Would you like to create a Django superuser? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Creating superuser..."
    python manage.py createsuperuser
    echo -e "${GREEN}✓ Superuser created${NC}"
else
    echo "Skipping superuser creation"
    echo "You can create one later with: python manage.py createsuperuser"
fi
echo ""

# Frontend Setup
echo "========================================"
echo "Setting up Frontend (React)"
echo "========================================"
echo ""

cd frontend

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
echo ""

cd ..

# Create convenience scripts
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start both servers:"
echo "   ${GREEN}./dev.sh${NC}"
echo ""
echo "2. Or start them separately:"
echo "   Backend:  ${GREEN}./run-backend.sh${NC}  (http://localhost:8000)"
echo "   Frontend: ${GREEN}./run-frontend.sh${NC} (http://localhost:3000)"
echo ""
echo "3. Access the application:"
echo "   Frontend: ${GREEN}http://localhost:3000${NC}"
echo "   Backend:  ${GREEN}http://localhost:8000/api/${NC}"
echo "   Admin:    ${GREEN}http://localhost:8000/admin/${NC}"
echo ""
echo -e "${YELLOW}Note: Make sure to activate the virtual environment before running backend commands:${NC}"
echo "   ${GREEN}source venv/bin/activate${NC}"
echo ""
