# Frontend: The Dining Room (React)

This is the "dining room" of our application—it's what the user sees and interacts with. It is built with **React** and **Vite**, a modern and fast build tool.

Think of this project as a **LEGO set**:

- **`index.html` & `main.tsx` - The Baseplate:** These files are the foundation. `index.html` provides the single HTML page, and `main.tsx` is the entry point that tells React where to start building.

- **`App.tsx` - The Main Instruction Manual:** This is the top-level component. It sets up the overall layout of the application (like the navigation bar) and defines the different "pages" using React Router.

- **`pages/` - The Rooms of Your Building:** Each file in this folder is a major page or view in our app, like the list of all patients or the detail view for a single patient. Each page is its own large LEGO creation.

- **Components - The LEGO Bricks:** While we don't have a separate `components/` folder in this simple project, a larger app would. Components are reusable pieces of UI—the individual bricks. A button, a form input, or a patient card are all components.

- **`api.ts` - The Walkie-Talkie:** This file is responsible for all communication with the backend. It contains organized, reusable functions for fetching, creating, and updating data. It's like a walkie-talkie pre-programmed with all the right channels to talk to the kitchen (the backend).

- **`types.ts` - The LEGO Piece Guide:** This file defines the "shape" of our data using TypeScript interfaces. It's like the guide in the instruction manual that shows you what each LEGO piece looks like, ensuring we use the right data in the right places.

## Key Design Choices (Good Habits to Learn)

We've made some specific choices in this frontend to teach good development habits.

### Environment Variables for Configuration (`.env.development`)

In `api.ts`, the backend URL is loaded from `import.meta.env.VITE_API_BASE_URL`.

- **Why?** Hardcoding URLs is a bad idea. The backend URL might be different on your machine, on a coworker's machine, or in production. Environment variables let you configure the application for different environments without changing the code. Vite uses files like `.env` or `.env.development` to manage this.

### Centralized API Logic (`api.ts`)

All the code for making API calls is in one place.

- **Why?** This makes the code much easier to manage. If you need to change how authentication works or update an endpoint, you only have to do it in one file. Your components stay clean and focused on displaying the UI, not on the details of HTTP requests.

### Type Safety (`types.ts`)

We use TypeScript to define interfaces for our data, like `Patient` and `MedicalRecord`.

- **Why?** This helps prevent bugs. If you accidentally try to use a field that doesn't exist (e.g., `patient.age` instead of `patient.date_of_birth`), TypeScript will warn you immediately, saving you from errors in the browser.

## How to Run Frontend Commands

Navigate to the frontend directory first:

```bash
cd frontend
```

- **Install dependencies (if you haven't run the main `setup.py`):**

  ```bash
  npm install
  ```

- **Run the frontend dev server only:**

  ```bash
  npm run dev
  ```

- **Build the frontend for production:**
  ```bash
  npm run build
  ```
