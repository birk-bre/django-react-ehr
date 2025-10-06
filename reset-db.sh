#!/bin/bash

# Patient EHR System - Quick Reset Script
# Resets the database to a clean state

set -e

echo "========================================"
echo "Database Reset Script"
echo "========================================"
echo ""
echo "⚠️  WARNING: This will delete all data in the database!"
echo ""
read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirmation

if [ "$confirmation" != "yes" ]; then
    echo "Reset cancelled."
    exit 0
fi

echo ""
echo "Resetting database..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Remove existing database
if [ -f "db.sqlite3" ]; then
    echo "Removing old database..."
    rm db.sqlite3
    echo "✓ Database removed"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate
echo "✓ Migrations completed"

echo ""
echo "Would you like to create a new superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
    echo "✓ Superuser created"
fi

echo ""
echo "========================================"
echo "Database reset complete!"
echo "========================================"
