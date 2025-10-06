# Frontend: React + TypeScript# Frontend: The Dining Room (React)

The frontend is built with React, TypeScript, and Vite. It provides the user interface for interacting with the EHR system and communicates with the backend via REST API calls.This is the "dining room" of our application—it's what the user sees and interacts with. It is built with **React** and **Vite**, a modern and fast build tool.

## Technology StackTo understand what React is please read the [official React documentation](https://react.dev/learn).

- **React 19**: UI library for building component-based interfacesThink of this project as a **LEGO set**:

- **TypeScript**: Type-safe JavaScript with compile-time error checking

- **Vite**: Fast build tool and development server- **`index.html` & `main.tsx` - The Baseplate:** These files are the foundation. `index.html` provides the single HTML page, and `main.tsx` is the entry point that tells React where to start building.

- **React Router**: Client-side routing for navigation

- **`App.tsx` - The Main Instruction Manual:** This is the top-level component. It sets up the overall layout of the application (like the navigation bar) and defines the different "pages" using React Router.

## Architecture Components

- **`pages/` - The Rooms of Your Building:** Each file in this folder is a major page or view in our app, like the list of all patients or the detail view for a single patient. Each page is its own large LEGO creation.

### Entry Points

- **Components - The LEGO Bricks:** While we don't have a separate `components/` folder in this simple project, a larger app would. Components are reusable pieces of UI—the individual bricks. A button, a form input, or a patient card are all components.

**`index.html`**

The single HTML page that serves as the application shell. React mounts to the `#root` div.- **`api.ts` - The Walkie-Talkie:** This file is responsible for all communication with the backend. It contains organized, reusable functions for fetching, creating, and updating data. It's like a walkie-talkie pre-programmed with all the right channels to talk to the kitchen (the backend).

**`main.tsx`** - **`types.ts` - The LEGO Piece Guide:** This file defines the "shape" of our data using TypeScript interfaces. It's like the guide in the instruction manual that shows you what each LEGO piece looks like, ensuring we use the right data in the right places.

The JavaScript entry point that renders the root React component:

````tsx## Key Design Choices (Good Habits to Learn)

ReactDOM.createRoot(document.getElementById('root')!).render(

  <React.StrictMode>We've made some specific choices in this frontend to teach good development habits.

    <App />

  </React.StrictMode>### Environment Variables for Configuration (`.env.development`)

)

```In `api.ts`, the backend URL is loaded from `import.meta.env.VITE_API_BASE_URL`.



### Core Application- **Why?** Hardcoding URLs is a bad idea. The backend URL might be different on your machine, on a coworker's machine, or in production. Environment variables let you configure the application for different environments without changing the code. Vite uses files like `.env` or `.env.development` to manage this.



**`App.tsx`**  ### Centralized API Logic (`api.ts`)

The root component that sets up:

- Application-wide layout and navigationAll the code for making API calls is in one place.

- React Router configuration

- Route definitions for different pages- **Why?** This makes the code much easier to manage. If you need to change how authentication works or update an endpoint, you only have to do it in one file. Your components stay clean and focused on displaying the UI, not on the details of HTTP requests.



```tsx### Type Safety (`types.ts`)

<BrowserRouter>

  <Routes>We use TypeScript to define interfaces for our data, like `Patient` and `MedicalRecord`.

    <Route path="/" element={<Patients />} />

    <Route path="/patient/:id" element={<PatientDetail />} />- **Why?** This helps prevent bugs. If you accidentally try to use a field that doesn't exist (e.g., `patient.age` instead of `patient.date_of_birth`), TypeScript will warn you immediately, saving you from errors in the browser.

  </Routes>

</BrowserRouter>## How to Run Frontend Commands

````

Navigate to the frontend directory first:

### Pages (`pages/`)

```bash

Pages represent distinct views in the application:cd frontend

```

**`Patients.tsx`**

- Lists all patients- **Install dependencies (if you haven't run the main `setup.py`):**

- Provides search and filtering

- Form for creating new patients ```bash

- Links to individual patient details npm install

  ```

  ```

**`PatientDetail.tsx`**

- Displays comprehensive patient information- **Run the frontend dev server only:**

- Shows medical records, medications, vital signs, and appointments

- Allows adding new records ```bash

  npm run dev

### API Layer (`api.ts`) ```

Centralized module for all backend communication. Key features:- **Build the frontend for production:**

````bash

```typescript  npm run build

const apiFetch = async <T>(endpoint: string, options?: RequestInit): Promise<T> => {  ```

// Handles fetch, errors, and response parsing
}

export const patientAPI = {
getAll: () => apiFetch<PaginatedResponse<Patient>>("/patients/"),
getOne: (id) => apiFetch<Patient>(`/patients/${id}/`),
create: (data) => apiFetch<Patient>("/patients/", { method: "POST", ... }),
// ...
}
````

**Benefits:**

- Single source of truth for API endpoints
- Consistent error handling
- Easy to mock for testing
- Type-safe API calls

### Type Definitions (`types.ts`)

TypeScript interfaces define the shape of data:

```typescript
export interface Patient {
  id: number;
  medical_record_number: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  // ...
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
```

**Benefits:**

- Autocomplete in your IDE
- Compile-time type checking
- Self-documenting code
- Catches errors before runtime

## React Patterns Used

### Hooks

**`useState`** - Managing component state:

```tsx
const [patients, setPatients] = useState<Patient[]>([]);
const [loading, setLoading] = useState<boolean>(true);
```

**`useEffect`** - Side effects (data fetching):

```tsx
useEffect(() => {
  loadPatients();
}, []); // Empty dependency array = run once on mount
```

**`useParams`** - Accessing route parameters:

```tsx
const { id } = useParams();
```

### Event Handling

```tsx
const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
  setFormData({ ...formData, [e.target.name]: e.target.value });
};

const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  await patientAPI.create(formData);
};
```

### Conditional Rendering

```tsx
{
  loading && <div className="loading">Loading...</div>;
}
{
  showForm && <form>...</form>;
}
{
  patients.map((patient) => <PatientCard key={patient.id} {...patient} />);
}
```

## Configuration

### Environment Variables

Create a `.env.development` file for local development:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Access in code:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
```

⚠️ **Never commit `.env` files with secrets**. Always use `.env.example` as a template.

### Vite Configuration (`vite.config.ts`)

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
```

## Common Patterns and Anti-Patterns

### ✅ Good Practices

**Centralized API calls**

```typescript
// Good - in api.ts
export const patientAPI = { ... }

// Usage in component
const patients = await patientAPI.getAll();
```

**Type-safe state**

```typescript
const [patient, setPatient] = useState<Patient | null>(null);
```

**Proper error handling**

```typescript
try {
  await patientAPI.create(data);
} catch (error) {
  // Show user-friendly error message
}
```

### ❌ Anti-Patterns to Avoid

**Using `alert()` for user feedback**

```typescript
// Bad - current implementation
alert("Error creating patient");

// Better - use toast notifications or inline error messages
setError("Failed to create patient. Please try again.");
```

**No loading states for async operations**

```typescript
// Bad
const handleSubmit = async () => {
  await patientAPI.create(data);
};

// Better
const handleSubmit = async () => {
  setSubmitting(true);
  try {
    await patientAPI.create(data);
  } finally {
    setSubmitting(false);
  }
};
```

**Console.error for production errors**

```typescript
// Bad
console.error("Error:", error);

// Better - implement error tracking (Sentry, LogRocket)
errorTracker.captureException(error);
```

## Development Workflow

### Running the Development Server

```bash
cd frontend
npm run dev
```

Server runs at `http://localhost:3000` with hot module replacement (HMR).

### Building for Production

```bash
npm run build
```

Creates optimized production build in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Extending the Frontend

### Adding a New Page

1. Create a new component in `pages/`
2. Add route in `App.tsx`
3. Add navigation link

Example:

```tsx
// pages/Dashboard.tsx
export default function Dashboard() {
  return <div>Dashboard</div>;
}

// App.tsx
<Route path="/dashboard" element={<Dashboard />} />;
```

### Adding Form Validation

```tsx
const [errors, setErrors] = useState<Record<string, string>>({});

const validateForm = (): boolean => {
  const newErrors: Record<string, string> = {};

  if (!formData.first_name) {
    newErrors.first_name = "First name is required";
  }

  if (!formData.email.includes("@")) {
    newErrors.email = "Invalid email format";
  }

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};

const handleSubmit = async (e: FormEvent) => {
  e.preventDefault();
  if (!validateForm()) return;
  // Submit form
};
```

### Adding Error Boundaries

Error boundaries catch React errors and display fallback UI:

```tsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}
```

### Creating Reusable Components

Extract repeated UI patterns:

```tsx
// components/Button.tsx
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  variant?: "primary" | "secondary";
}

export function Button({
  onClick,
  children,
  variant = "primary",
}: ButtonProps) {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {children}
    </button>
  );
}
```

## Common Issues and Solutions

### CORS Errors

If you see CORS errors, ensure:

- Backend CORS settings allow your frontend origin
- API_BASE_URL is correctly configured
- Backend server is running

### Type Errors

```bash
# Regenerate TypeScript types after API changes
npm run build
```

### Module Not Found

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Hot Reload Not Working

- Save the file
- Check console for errors
- Restart dev server: `npm run dev`

## Further Reading

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Router Tutorial](https://reactrouter.com/en/main/start/tutorial)
- [React Patterns](https://reactpatterns.com/)
