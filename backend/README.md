# Backend: The Restaurant Kitchen (Django)

Welcome to the backend! This is the "kitchen" of our application. It’s powered by **Django** and the **Django REST Framework**, and its job is to handle business logic, manage the database, and provide data to the frontend through an API.

Using our restaurant analogy, here's how the kitchen is organized:

- **`models.py` - The Pantry & Ingredients:** This file defines the structure of our data. Each class is like a blueprint for an ingredient (e.g., a `Patient` or a `Medication`). Django uses these models to create our database tables.

- **`views.py` - The Chefs:** The views are our chefs. When a request (an order) comes in from the API, a view is responsible for handling it. It might fetch data from the database, create new records, or update existing ones.

- **`serializers.py` - The Universal Translator:** Our frontend speaks JavaScript (JSON), and our backend speaks Python. The serializers are translators that convert data between these two languages, ensuring they can understand each other.

- **`urls.py` - The Order Window:** This file defines all the available API endpoints. It's like the window where the waiter (`API`) places an order with the kitchen. It maps each URL to a specific "chef" (`view`).

- **`admin.py` - The Health Inspector:** Django comes with a built-in admin site, a powerful tool for viewing and managing your data directly. You can register your models here to make them accessible in the admin panel.

## Key Design Choices (Good Habits to Learn)

We've made some specific choices in this backend to teach good development habits.

### Explicit is Better Than Implicit (`serializers.py`)

You might see `fields = '__all__'` in other Django projects. We intentionally avoid this.

- **Why?** Explicitly listing fields (e.g., `fields = ['id', 'first_name', ...]`) is more secure. If you add a sensitive field to your model later (like a password or personal ID), `'__all__'` would automatically expose it through the API. Listing fields manually forces you to be intentional about what data you share.

### Keep it DRY (Don't Repeat Yourself)

In our `views.py`, you might notice that the `get_queryset` method for filtering by patient ID is similar across different views. For this learning project, we've kept them separate to be clear and explicit. 

- **As a next step, how could you improve this?** You could create a reusable **Mixin**. A mixin is a class that you can "mix in" to your views to share common functionality without having to write it over and over. This is a great way to keep your code clean and maintainable.

### Database Seeding (`management/commands/seed_db.py`)

An empty application isn't very interesting. We've included a `seed_db` command to populate your database with realistic sample data. This is a common practice that makes development and testing much easier.

## How to Run Backend Commands

First, make sure you activate the Python virtual environment. This isolates the project's dependencies.

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

Now you can run standard Django commands:

- **Apply database migrations:**
  ```bash
  python manage.py migrate
  ```

- **Create a new migration (after changing `models.py`):**
  ```bash
  python manage.py makemigrations
  ```

- **Run the backend server only:**
  ```bash
  python manage.py runserver
  ```

- **Seed the database with sample data:**
  ```bash
  python manage.py seed_db
  ```
