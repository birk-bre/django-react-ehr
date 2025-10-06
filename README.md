# Patient EHR System

A full-stack Electronic Health Records (EHR) learning project built with Django REST Framework and React.

> **Note:** This project is designed for learning Django, React, and full-stack development. It's intentionally kept simple and straightforward.

## What You'll Learn

- **Django:** Models, Views, Serializers, REST APIs
- **React:** Components, Hooks, Routing, API Integration
- **Full-Stack:** Frontend-Backend communication, CORS, Database design

## Project Structure

```
PatientEHR/
├── backend/           # Django backend
│   └── ehr/          # EHR app (models, views, serializers)
├── frontend/         # React frontend
│   └── src/          # React components and pages
├── manage.py         # Django CLI
└── db.sqlite3        # SQLite database
```

## Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)

Check your installations:

```bash
python3 --version
node --version
```

## Quick Start

### 1. Setup (First Time)

```bash
python setup.py
```

This installs everything and sets up the database. Works on Windows, macOS, and Linux.

### 2. Run the Application

```bash
python dev.py
```

This will show you a menu with options to:

- Start development servers (backend + frontend)
- Reset database
- Seed database with sample data

### 3. Manual Server Management (Optional)

If you prefer to run servers separately, you can still do so after setup by activating the virtual environment:

**macOS/Linux:**

```bash
source venv/bin/activate
python manage.py runserver 8000        # Backend
```

**Windows:**

```bash
venv\Scripts\activate
python manage.py runserver 8000        # Backend
```

**Frontend (all platforms):**

```bash
cd frontend
npm run dev                             # Frontend
```

### 3. Access the App

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/

## How It Works

### Backend (Django)

- **Models** (`backend/ehr/models.py`) - Define database structure
- **Serializers** (`backend/ehr/serializers.py`) - Convert data to/from JSON
- **Views** (`backend/ehr/views.py`) - Handle API requests
- **URLs** (`backend/ehr/urls.py`) - Define API endpoints

### Frontend (React)

- **API calls** (`frontend/src/api.js`) - Communicate with backend
- **Pages** (`frontend/src/pages/`) - UI components
- **Routing** - Navigate between pages

### Communication

Frontend (port 5000) → API calls → Backend (port 8000) → Database

## Learning Exercises

Here are some things to try:

1. **Add a new field to Patient model**

   - Edit `backend/ehr/models.py`
   - Run `python manage.py makemigrations`
   - Run `python manage.py migrate`

2. **Create a new API endpoint**

   - Add a view in `backend/ehr/views.py`
   - Add URL in `backend/ehr/urls.py`

3. **Build a new React page**
   - Create component in `frontend/src/pages/`
   - Add route in `frontend/src/App.jsx`
   - Use API from `frontend/src/api.js`

## Common Commands

**Backend:**

```bash
source venv/bin/activate              # Activate Python environment
python manage.py makemigrations       # Create database migrations
python manage.py migrate              # Apply migrations
python manage.py createsuperuser      # Create admin user
python manage.py shell                # Django shell
```

**Frontend:**

```bash
cd frontend
npm run dev                           # Start dev server
npm run build                         # Build for production
```

## Reset Database

If you want to start fresh, run the development manager:

```bash
python dev.py
```

Then select option 2 "Reset Database" from the menu. This deletes the database and creates a new one.

## Sample Data

To populate your database with sample patients and records for testing:

```bash
python dev.py
```

Then select option 3 "Seed Database with Sample Data" from the menu.

## Troubleshooting

**"No module named 'django'"**

- Activate virtual environment: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

**"Port already in use"**

- Backend: `lsof -ti:8000 | xargs kill -9`
- Frontend: `lsof -ti:3000 | xargs kill -9`

**Database errors**

- Run: `python manage.py migrate`
- Or reset: `./reset-db.sh`

**Frontend can't reach backend**

- Make sure backend is running on port 8000
- Check browser console for errors

## Tech Stack

- Django 5.2.7 + Django REST Framework
- React 19.1.1 + Vite 7.1.7
- SQLite database

## Next Steps

- Explore the code in `backend/ehr/` and `frontend/src/`
- Read Django docs: https://docs.djangoproject.com/
- Read React docs: https://react.dev/
- Experiment and break things - that's how you learn!

---

**Remember:** This is a learning project. Don't worry about production concerns - focus on understanding how Django and React work together!
