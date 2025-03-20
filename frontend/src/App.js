import { useState } from "react";
import './App.css';
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import HomePage from "./components/HomePage";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? children : <Navigate to="/" replace />; 
};

function App() {
  const [user, setUser] = useState(null);
  
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Login Page (Default) */}
            <Route path="/" element={<LoginForm setUser={setUser} />} />

            {/* Register Page */}
            <Route path="/register" element={<RegisterForm setUser={setUser} />} />

            {/* Protected Home Page */}
            <Route path="/home" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />

            {/* Redirect all other paths to "/" */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
