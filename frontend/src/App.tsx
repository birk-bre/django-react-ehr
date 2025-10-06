import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Patients from "./pages/Patients";
import PatientDetail from "./pages/PatientDetail";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="container">
            <Link to="/" className="logo">
              <h1>EHR System</h1>
            </Link>
            <div className="nav-links">
              <Link to="/">Patients</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Patients />} />
            <Route path="/patient/:id" element={<PatientDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
