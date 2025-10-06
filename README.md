# Full-Stack EHR System: React + Django

A production-oriented Electronic Health Record (EHR) system demonstrating modern full-stack development practices. This project serves as a practical foundation for understanding how frontend and backend systems communicate in real-world applications.

## Learning Objectives

This project will help you understand:

- **Client-Server Architecture**: How frontend applications communicate with backend APIs over HTTP
- **RESTful API Design**: Best practices for structuring API endpoints and data flow
- **State Management**: Managing application state and side effects in React
- **Data Modeling**: Designing relational database schemas with Django ORM
- **Type Safety**: Using TypeScript to catch errors before runtime
- **Development Workflow**: Setting up and maintaining a modern development environment

## Architecture Overview

### Frontend (React + TypeScript)

The client application handles the user interface and user interactions. Built with React and Vite for fast development and optimized production builds.

**Key responsibilities:**

- Rendering the user interface
- Managing application state
- Making HTTP requests to the backend API
- Handling user input and validation

See [frontend README](frontend/README.md) for detailed documentation.

### Backend (Django + Django REST Framework)

The server application manages business logic, data persistence, and API endpoints. Built with Django for robust database handling and Django REST Framework for API development.

**Key responsibilities:**

- Defining data models and database schema
- Processing and validating incoming requests
- Enforcing business rules and data integrity
- Serving data through RESTful API endpoints

See [backend README](backend/README.md) for detailed documentation.

### API Layer

The communication protocol between frontend and backend follows REST principles, using JSON for data serialization. The API handles:

- Patient management (CRUD operations)
- Medical records, medications, vital signs, and appointments
- Query filtering and pagination
- Data validation and error responses

# Full-Stack app with React & Django

This project is a simple Electronic Health Record (EHR) system built with a React frontend and a Django backend.

Think of this project as a restaurant:

- **The Frontend (React)** is the **dining room**. It's everything the customer (user) sees and interacts with—the tables, the menus, the decor. It's built to be pleasant and intuitive. Read the [frontend README](frontend/README.md) for more details.

- **The Backend (Django)** is the **kitchen**. It's where the food is made, where the orders are processed, and where all the important ingredients are stored. The customer doesn't see the kitchen, but it's essential for the restaurant to function. Read the [backend README](backend/README.md) for more details.

- **The API (Django REST Framework)** is the **waiter**. The waiter takes orders from the dining room, brings them to the kitchen, and then delivers the finished dishes back to the table. It’s the critical communication link between the frontend and backend.

This project is intentionally kept simple so you can focus on learning the core concepts of full-stack development without getting lost.

- **Core Concepts:** Understand how a frontend client and a backend server talk to each other.
- **Backend Development:** Learn the basics of Django, including creating data models, writing API views, and using serializers to handle data.
- **Frontend Development:** Learn the basics of React, including creating components, managing state with hooks, fetching data from an API, and navigating between pages.
- **Database Management:** See how to define a database structure and populate it with initial data.

## Prerequisites

Ensure you have the following installed:

- **Python 3.11+** - Backend runtime environment ([Download](https://python.org/))
- **Node.js 18+** - Frontend runtime environment ([Download](https://nodejs.org/))

Verify installations:

```bash
python3 --version
node --version
```

## Quick Start

### Initial Setup

Run the automated setup script to install all dependencies and configure the database:

```bash
python setup.py
```

This script will:

- Create a Python virtual environment
- Install backend dependencies
- Run database migrations
- Install frontend dependencies
- Offer to create a Django superuser account

### Running the Application

Use the development manager to start both servers:

```bash
python dev.py
```

Or start them individually:

```bash
# Terminal 1 - Backend server
python manage.py runserver

# Terminal 2 - Frontend server (in frontend/ directory)
npm run dev
```

**Access points:**

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000/api/](http://localhost:8000/api/)
- Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Project Structure

```
PatientEHR/
├── backend/              # Django application
│   ├── ehr/              # Main Django app
│   │   ├── models.py     # Database models (Patient, MedicalRecord, etc.)
│   │   ├── serializers.py# REST serializers for JSON conversion
│   │   ├── views.py      # API ViewSets (business logic)
│   │   ├── urls.py       # API endpoint routing
│   │   └── admin.py      # Django admin configuration
│   ├── settings.py       # Django configuration
│   └── README.md         # Backend documentation
│
├── frontend/             # React application
│   ├── src/
│   │   ├── pages/        # Page components (Patients, PatientDetail)
│   │   ├── api.ts        # API client functions
│   │   ├── types.ts      # TypeScript type definitions
│   │   └── App.tsx       # Root component with routing
│   └── README.md         # Frontend documentation
│
├── dev.py                # Development server manager
├── setup.py              # Initial project setup script
└── README.md             # This file
```

## Key Design Patterns

### Backend Patterns

**ViewSets with DRF Router**  
Using Django REST Framework's ViewSets provides standardized CRUD operations with minimal code. The router automatically generates URL patterns.

**Explicit Serializer Fields**  
Serializers explicitly list fields rather than using `fields = '__all__'`. This prevents accidentally exposing sensitive data when models are extended.

**Query Parameter Filtering**  
ViewSets support filtering via query parameters (e.g., `/api/medications/?patient=1`), allowing flexible data retrieval without custom endpoints.

### Frontend Patterns

**Centralized API Layer**  
All API calls are organized in `api.ts`, separating concerns and making the codebase easier to maintain and test.

**Type-Safe Data Structures**  
TypeScript interfaces in `types.ts` provide compile-time type checking, reducing runtime errors and improving developer experience.

**Environment-Based Configuration**  
Using environment variables (`.env` files) allows different configurations for development, staging, and production without code changes.

## Development Best Practices

### Security Considerations

⚠️ This project prioritizes clarity over production-ready security. In a production environment, you should:

- Use environment variables for all secrets (never commit `.env` files)
- Implement authentication and authorization (JWT, OAuth, Django sessions)
- Enable HTTPS in production
- Set `DEBUG = False` and restrict `ALLOWED_HOSTS`
- Use proper CORS configuration (not `CORS_ALLOW_ALL_ORIGINS`)
- Implement rate limiting and input sanitization
- Regular security audits and dependency updates

### Code Quality

**DRY Principle (Don't Repeat Yourself)**  
We use a `PatientFilterMixin` (in `backend/ehr/mixins.py`) to avoid repeating patient filtering logic across ViewSets. This mixin provides a reusable `get_queryset` method that filters resources by patient ID via query parameters.

**Why use mixins?**

- **Single Source of Truth**: Filtering logic is defined once and reused across multiple ViewSets
- **Maintainability**: Changes to filtering behavior only need to be made in one place
- **Testability**: Mixin behavior can be tested independently
- **Flexibility**: ViewSets can override or extend the mixin's behavior as needed

**Example usage:**

```python
class MedicalRecordViewSet(PatientFilterMixin, viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    # Inherits patient filtering from the mixin
```

**Error Handling**  
The current implementation has basic error handling.

## Area for Improvement

### Low hanging fruit

1. **Add a Field to Patient Model**

   - Add a `middle_name` field to the `Patient` model
   - Update the serializer and migration
   - Display it in the frontend

2. **Create a Filter**
   - Add blood type filtering to the patients list
   - Use Django's filter backends
   - Update the frontend to use the filter

### Time consuming

3. **Study the Mixin Pattern**

   - Review `backend/ehr/mixins.py` to understand the `PatientFilterMixin`
   - See how it's used in `views.py` to eliminate code duplication
   - Create your own mixin for common functionality (e.g., date range filtering)

4. **Add Form Validation**
   - Implement client-side form validation in React
   - Add visual feedback for validation errors
   - Ensure server-side validation catches edge cases

### Very time consuming

5. **Add Authentication**

   - Implement JWT authentication with Django REST Framework SimpleJWT
   - Protect API endpoints with permissions
   - Add login/logout functionality to the frontend

6. **Create a Dashboard**
   - Build a dashboard page showing statistics
   - Display charts using a library like Chart.js or Recharts
   - Aggregate data efficiently in Django

## Common Issues and Solutions

### Backend Issues

**Migration conflicts**

```bash
python manage.py migrate --fake
python manage.py migrate
```

**Port already in use**

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use a different port
python manage.py runserver 8001
```

### Frontend Issues

**Module not found errors**

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Port 3000 in use**

```bash
# Vite will automatically prompt to use a different port
# Or set a custom port in vite.config.ts
```

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Guide](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [REST API Best Practices](https://restfulapi.net/)
