# Backend: Django REST API# Backend: The Restaurant Kitchen (Django)

The backend is built with Django and Django REST Framework (DRF), providing a RESTful API for the EHR system. It handles data persistence, business logic, and API endpoint management.Welcome to the backend! This is the "kitchen" of our application. It’s powered by **Django** and the **Django REST Framework**, and its job is to handle business logic, manage the database, and provide data to the frontend through an API.

## Architecture ComponentsUsing our restaurant analogy, here's how the kitchen is organized:

### Models (`models.py`)- **`models.py` - The Pantry & Ingredients:** This file defines the structure of our data. Each class is like a blueprint for an ingredient (e.g., a `Patient` or a `Medication`). Django uses these models to create our database tables.

Django models define the database schema using Python classes. Each model represents a table, and each field represents a column. Key models:- **`views.py` - The Chefs:** The views are our chefs. When a request (an order) comes in from the API, a view is responsible for handling it. It might fetch data from the database, create new records, or update existing ones.

- **Patient**: Core entity with demographics and contact information- **`serializers.py` - The Universal Translator:** Our frontend speaks JavaScript (JSON), and our backend speaks Python. The serializers are translators that convert data between these two languages, ensuring they can understand each other.

- **MedicalRecord**: Visit history and diagnoses

- **Medication**: Prescription tracking- **`urls.py` - The Order Window:** This file defines all the available API endpoints. It's like the window where the waiter (`API`) places an order with the kitchen. It maps each URL to a specific "chef" (`view`).

- **VitalSign**: Health measurements over time

- **Appointment**: Scheduling and status tracking- **`admin.py` - The Health Inspector:** Django comes with a built-in admin site, a powerful tool for viewing and managing your data directly. You can register your models here to make them accessible in the admin panel.

**Design choices:**## Key Design Choices (Good Habits to Learn)

- `auto_now_add` and `auto_now` for automatic timestamp management

- `related_name` for reverse foreign key relationshipsWe've made some specific choices in this backend to teach good development habits.

- Validators for data integrity at the database level

- Choices for enumerated fields (gender, blood type, status)### Explicit is Better Than Implicit (`serializers.py`)

### ViewSets (`views.py`)You might see `fields = '__all__'` in other Django projects. We intentionally avoid this.

ViewSets combine the logic for multiple related views (list, create, retrieve, update, delete). They provide:- **Why?** Explicitly listing fields (e.g., `fields = ['id', 'first_name', ...]`) is more secure. If you add a sensitive field to your model later (like a password or personal ID), `'__all__'` would automatically expose it through the API. Listing fields manually forces you to be intentional about what data you share.

- Standardized CRUD operations### Keep it DRY (Don't Repeat Yourself)

- Query parameter filtering

- Search functionalityIn our `views.py`, you might notice that the `get_queryset` method for filtering by patient ID is similar across different views. For this learning project, we've kept them separate to be clear and explicit.

- Ordering capabilities

- **As a next step, how could you improve this?** You could create a reusable **Mixin**. A mixin is a class that you can "mix in" to your views to share common functionality without having to write it over and over. This is a great way to keep your code clean and maintainable.

**Current implementation:**

```python### Database Seeding (`management/commands/seed_db.py`)

class PatientViewSet(viewsets.ModelViewSet):

    queryset = Patient.objects.all()An empty application isn't very interesting. We've included a `seed_db` command to populate your database with realistic sample data. This is a common practice that makes development and testing much easier.

    serializer_class = PatientSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]## How to Run Backend Commands

    search_fields = ['first_name', 'last_name', 'medical_record_number']

````First, make sure you activate the Python virtual environment. This isolates the project's dependencies.



### Serializers (`serializers.py`)**macOS/Linux:**

```bash

Serializers handle the conversion between complex data types (like Django models) and Python primitives that can be rendered into JSON. They also handle deserialization and validation.source venv/bin/activate

````

**Key principle: Explicit field declaration**

**Windows:**

Instead of `fields = '__all__'`, we explicitly list fields:```bash

venv\Scripts\activate

`python`

class PatientSerializer(serializers.ModelSerializer):

    class Meta:Now you can run standard Django commands:

        model = Patient

        fields = ['id', 'medical_record_number', 'first_name', ...]- **Apply database migrations:**

`  `bash

python manage.py migrate

**Why?** This prevents accidentally exposing sensitive fields if you add them to the model later (e.g., SSN, internal notes). ```

### URL Configuration (`urls.py`)- **Create a new migration (after changing `models.py`):**

```bash

DRF's router automatically generates URL patterns for ViewSets:  python manage.py makemigrations

```

````python

router = DefaultRouter()- **Run the backend server only:**

router.register(r'patients', PatientViewSet)  ```bash

```  python manage.py runserver

````

This creates:

- `GET /api/patients/` - List all patients- **Seed the database with sample data:**

- `POST /api/patients/` - Create a patient ```bash

- `GET /api/patients/{id}/` - Retrieve a patient python manage.py seed_db

- `PUT /api/patients/{id}/` - Update a patient ```

- `DELETE /api/patients/{id}/` - Delete a patient

### Admin Interface (`admin.py`)

Django's admin provides a web-based interface for data management. Registered models appear in the admin dashboard at `/admin/`.

## Design Patterns and Best Practices

### DRY Violation: Repeated Query Filtering

Notice the similar `get_queryset` methods across ViewSets:

```python
def get_queryset(self):
    queryset = MedicalRecord.objects.all()
    patient_id = self.request.query_params.get('patient')
    if patient_id:
        queryset = queryset.filter(patient_id=patient_id)
    return queryset
```

**This is intentional for learning**, but violates the DRY (Don't Repeat Yourself) principle.

**Better approach**: Create a mixin:

```python
class PatientFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset

class MedicalRecordViewSet(PatientFilterMixin, viewsets.ModelViewSet):
    # Inherits filtering logic
    pass
```

### Security Considerations

⚠️ **Current configuration is for development only**

The project has several security shortcuts appropriate for learning but not for production:

1. **AllowAny Permissions**: All API endpoints are publicly accessible
   - Production: Use `IsAuthenticated`, `IsAdminUser`, or custom permissions
2. **CORS Allow All**: Any origin can make requests

   - Production: Specify exact allowed origins in `CORS_ALLOWED_ORIGINS`

3. **DEBUG Mode**: Exposes detailed error messages

   - Production: Set `DEBUG = False` and configure proper error pages

4. **Secret Key**: Uses a default value

   - Production: Generate a unique secret key and store in environment variables

5. **SQLite Database**: Single-file database
   - Production: Use PostgreSQL or MySQL for better performance and features

### Database Seeding

The `management/commands/seed_db.py` command populates the database with realistic sample data using Faker. This is useful for:

- Development and testing
- Demonstrating the application
- Providing data for learning exercises

Run it with:

```bash
python manage.py seed_db
```

## API Examples

### List Patients with Search

```bash
GET /api/patients/?search=john
```

### Get Patient's Medical Records

```bash
GET /api/medical-records/?patient=1
```

### Get Active Medications for Patient

```bash
GET /api/medications/?patient=1&is_active=true
```

### Create a New Vital Sign

```bash
POST /api/vital-signs/
Content-Type: application/json

{
  "patient": 1,
  "recorded_at": "2024-01-15T10:30:00Z",
  "blood_pressure_systolic": 120,
  "blood_pressure_diastolic": 80,
  "heart_rate": 72,
  "temperature": 98.6,
  "weight": 150.5
}
```

## Running Backend Commands

Activate the virtual environment first:

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

**Common commands:**

```bash
# Run development server
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Populate database with sample data
python manage.py seed_db

# Open Django shell
python manage.py shell

# Run tests (when implemented)
python manage.py test
```

## Extending the Backend

### Adding a New Field

1. Update the model in `models.py`
2. Create and run migrations
3. Update the serializer to include the field
4. Update the admin registration if needed

Example:

```python
# models.py
class Patient(models.Model):
    middle_name = models.CharField(max_length=100, blank=True)
    # ... other fields

# serializers.py
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'first_name', 'middle_name', 'last_name', ...]
```

### Adding Custom Validation

```python
class PatientSerializer(serializers.ModelSerializer):
    def validate_phone(self, value):
        # Custom validation logic
        if not value.replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Phone must contain only digits")
        return value
```

### Adding Custom Endpoints

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class PatientViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        patient = self.get_object()
        return Response({
            'name': f"{patient.first_name} {patient.last_name}",
            'total_visits': patient.medical_records.count(),
            'active_medications': patient.medications.filter(is_active=True).count()
        })
```

Accessible at: `GET /api/patients/{id}/summary/`

## Production Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use environment variables for all secrets
- [ ] Switch to PostgreSQL or MySQL
- [ ] Configure CORS properly
- [ ] Implement authentication and permissions
- [ ] Set up HTTPS
- [ ] Configure static file serving
- [ ] Set up logging and monitoring
- [ ] Implement rate limiting
- [ ] Regular security audits
- [ ] Database backups
- [ ] Use a production WSGI server (Gunicorn, uWSGI)

## Further Reading

- [Django Documentation](https://docs.djangoproject.com/)
- [DRF ViewSets Guide](https://www.django-rest-framework.org/api-guide/viewsets/)
- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Django ORM Cookbook](https://books.agiliq.com/projects/django-orm-cookbook/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) (Book)
