# Patient EHR: Your First Full-Stack Adventure

This project is a simple Electronic Health Record (EHR) system designed to be your very first step into the world of building complete web applications.

Think of this project as a restaurant:

- **The Frontend (React)** is the **dining room**. It's everything the customer (user) sees and interacts with—the tables, the menus, the decor. It's built to be pleasant and intuitive.
- **The Backend (Django)** is the **kitchen**. It's where the food is made, where the orders are processed, and where all the important ingredients are stored. The customer doesn't see the kitchen, but it's essential for the restaurant to function.
- **The API (Django REST Framework)** is the **waiter**. The waiter takes orders from the dining room, brings them to the kitchen, and then delivers the finished dishes back to the table. It’s the critical communication link between the frontend and backend.

This project is intentionally kept simple so you can focus on learning the core concepts of full-stack development without getting lost.

- **Core Concepts:** Understand how a frontend client and a backend server talk to each other.
- **Backend Development:** Learn the basics of Django, including creating data models, writing API views, and using serializers to handle data.
- **Frontend Development:** Learn the basics of React, including creating components, managing state with hooks, fetching data from an API, and navigating between pages.
- **Database Management:** See how to define a database structure and populate it with initial data.

## Prerequisites

Before you begin, make sure you have the following installed. These are the essential tools for web development.

- **Python (v3.11+):** The language for our Django backend.
- **Node.js (v18+):** The environment for running our React frontend.

You can check if you have them installed by running:

```bash
python3 --version
node --version
```

## Quick Start

Getting the project running is as simple as two commands.

### 1. First-Time Setup

This command installs all dependencies for both the frontend and backend and sets up your database.

```bash
# This script handles everything for you!
python setup.py
```

### 2. Run the Application

This command starts both the backend and frontend development servers at the same time.

```bash
# This script gives you a handy menu to manage the project
python dev.py
```

Once the servers are running, you can access the application:

- **Frontend App:** [http://localhost:3000](http://localhost:3000)
- **Backend API:** [http://localhost:8000/api/](http://localhost:8000/api/)
- **Backend Admin Panel:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Project Structure

Here’s a map of the most important files and folders.

```
PatientEHR/
├── backend/              # The "Kitchen" (Django)
│   ├── ehr/              # The main Django app for our EHR system
│   │   ├── models.py     # Defines the database structure (the ingredients)
│   │   ├── serializers.py# Converts data to and from JSON (the translator)
│   │   ├── views.py      # Handles API requests (the chefs)
│   │   └── urls.py       # Defines the API endpoints (the order window)
│   └── README.md         # A guide to the backend
│
├── frontend/             # The "Dining Room" (React)
│   ├── src/
│   │   ├── pages/        # The different pages of our app (e.g., Patient List)
│   │   ├── api.ts        # Handles all communication with the backend (the phone line)
│   │   ├── types.ts      # Defines the shape of our data (the dictionary)
│   │   └── App.tsx       # The main component that holds our app layout and routing
│   └── README.md         # A guide to the frontend
│
├── dev.py                # Your friendly development script
├── setup.py              # The initial setup script
└── README.md             # You are here!
```

## Next Steps & Learning Exercises

Now that you're set up, it's time to explore! Here are a few ideas to get you started.

1.  **Add a New Field:** Try adding a `middle_name` to the `Patient` model in `backend/ehr/models.py`. You'll need to update the serializer and the frontend form to display it!
2.  **Create a New Page:** Build a new React page that shows a dashboard of upcoming appointments.
3.  **Explore the Code:** Read the `README.md` files in the `frontend` and `backend` folders to dive deeper into how each part works.

Don't be afraid to experiment and break things. That's the best way to learn!
