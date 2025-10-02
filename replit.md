# EHR System (Electronic Health Records)

## Overview

This is a full-stack Electronic Health Records (EHR) management system built with Django REST Framework on the backend and React with Vite on the frontend. The application allows healthcare providers to manage patient information, medical records, medications, vital signs, and appointments through a RESTful API and modern web interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: React 19.1.1 with Vite 7.1.7 as the build tool

**Rationale**: Vite provides fast development server startup and Hot Module Replacement (HMR), making the development experience smooth. React 19 offers the latest features and performance improvements.

**Key Technologies**:
- **React Router DOM** (v7.9.3): Client-side routing for navigation between patient records, appointments, and other views
- **Axios** (v1.12.2): HTTP client for making API requests to the Django backend
- **ESLint**: Code quality and consistency enforcement with React-specific rules

**Communication Pattern**: The frontend communicates with the backend via REST APIs. The API base URL is dynamically constructed to work in development (port 5000 for frontend, port 8000 for backend) by replacing the port in the origin URL.

**Pros**: 
- Fast development cycles with HMR
- Modern React features and hooks
- Clear separation of concerns with dedicated API layer

**Cons**:
- No state management library (Redux/Zustand) may become problematic as the app grows
- No TypeScript means less type safety

### Backend Architecture

**Framework**: Django 5.2.7 with Django REST Framework

**Rationale**: Django provides a robust ORM, built-in admin interface, and excellent security features. DRF simplifies building RESTful APIs with serialization, viewsets, and authentication.

**Design Pattern**: The application follows Django's MTV (Model-Template-View) pattern, adapted for API-first development:
- **Models**: Define the database schema for Patient, MedicalRecord, Medication, VitalSign, and Appointment
- **Serializers**: Handle conversion between Python objects and JSON
- **ViewSets**: Provide CRUD operations with filtering and search capabilities
- **URLs**: RESTful routing using DRF's DefaultRouter

**Key Features**:
- **ViewSets with filtering**: Search and ordering capabilities for patients, filtering by patient ID for related records
- **CORS enabled**: `corsheaders` middleware allows cross-origin requests from the frontend
- **Model relationships**: Foreign key relationships between Patient and related models (MedicalRecord, Medication, etc.)

**Security Configuration**:
- `ALLOWED_HOSTS = ['*']` - Currently allows all hosts (should be restricted in production)
- `DEBUG = True` - Debug mode enabled (should be False in production)
- Secret key is hardcoded (should use environment variables in production)

**Pros**:
- Django ORM handles complex queries and relationships
- Built-in admin interface for data management
- DRF provides consistent API patterns
- Excellent documentation and community support

**Cons**:
- No authentication/authorization currently implemented
- Security settings are development-focused and unsuitable for production

### Data Models

**Core Entities**:

1. **Patient**: Central entity containing demographic information
   - Unique medical record number
   - Personal details (name, DOB, gender, blood type)
   - Contact information (phone, email, address)
   - Emergency contact details

2. **MedicalRecord**: Visit history and diagnoses
   - Linked to Patient via foreign key
   - Contains visit date, complaints, diagnosis, treatment plan
   - Tracks doctor name and clinical notes

3. **Medication**: Prescription tracking (referenced but not fully shown)
   - Patient medications with dosage and frequency
   - Active/inactive status tracking

4. **VitalSign**: Health measurements (referenced but not fully shown)
   - Time-series data for patient vitals

5. **Appointment**: Scheduling system (referenced but not fully shown)
   - Patient appointment management

**Model Design Decisions**:
- Used Django's built-in choices for constrained fields (gender, blood type)
- Timestamps (created_at, updated_at) on all models for audit trails
- Ordering by creation date (newest first) for patients
- Validators for data integrity (referenced for VitalSign model)

### API Structure

**REST Endpoints**: All endpoints follow the pattern `/api/{resource}/`

**Resources**:
- `/api/patients/` - Patient CRUD with search functionality
- `/api/medical-records/` - Medical records filtered by patient
- `/api/medications/` - Medications with active status filtering
- `/api/vital-signs/` - Vital signs by patient
- `/api/appointments/` - Appointment scheduling

**Search & Filtering**: 
- Patients: Searchable by name, MRN, email
- Related records: Filterable by patient ID via query parameters
- Medications: Additional filtering by active status

**HTTP Methods**: Standard REST operations (GET, POST, PUT, PATCH, DELETE) supported via DRF ViewSets

## External Dependencies

### Backend Dependencies

**Core Framework**:
- **Django 5.2.7**: Web framework and ORM
- **Django REST Framework**: API development toolkit

**Middleware & Extensions**:
- **django-cors-headers**: Handles CORS for cross-origin requests from frontend

**Database**: 
- Default Django database (SQLite for development, likely PostgreSQL for production based on typical Django deployments)
- Django ORM handles all database interactions

### Frontend Dependencies

**Core Libraries**:
- **React 19.1.1**: UI library
- **React DOM 19.1.1**: React rendering
- **React Router DOM 7.9.3**: Client-side routing

**HTTP Client**:
- **Axios 1.12.2**: Promise-based HTTP client for API calls

**Development Tools**:
- **Vite 7.1.7**: Build tool and dev server
- **ESLint**: Linting with React-specific plugins
- **@vitejs/plugin-react**: Vite plugin for React support

### Server Configuration

**Frontend Server**:
- Vite dev server running on port 5000
- Configured with `host: '0.0.0.0'` for network access
- `strictPort: true` prevents fallback to other ports

**Backend Server**:
- Django development server (default port 8000)
- WSGI/ASGI configuration for deployment

### Missing Components

**Authentication**: No authentication system implemented (Django's built-in auth or JWT would be typical choices)

**Production Database**: Currently uses default Django database configuration (likely SQLite), would need PostgreSQL or similar for production

**Environment Configuration**: No environment variable management (would benefit from python-decoenv or similar)

**API Documentation**: No Swagger/OpenAPI documentation configured (drf-spectacular would be a good addition)