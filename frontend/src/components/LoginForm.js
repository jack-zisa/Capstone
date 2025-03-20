import { useState, useEffect } from "react";
import { loginUser, loginWithFitbit } from "../api";
import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"; // Import useNavigate

const LoginForm = ({ setUser }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const { isLoggedIn, setIsLoggedIn } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (isLoggedIn) navigate("/home"); // Redirect if already logged in
    }, [isLoggedIn, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        const response = await loginUser(username, password);

        if (response.success) {
            setIsLoggedIn(true)
            setUser(response.data); // Store user session
            navigate("/home");
        } else {
            setError(response.error);
        }
    };

    const handleFitbitLogin = async () => {
        const response = await loginWithFitbit();
        if (response.success) {
            setUser(response.data);
            navigate("/home");
        } else {
            setError(response.error);
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            {error && <p className="error">{error}</p>}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Login</button>
            </form>
            <button onClick={() => navigate("/register")}>Register New Account</button>
            <button onClick={handleFitbitLogin} className="fitbit-button">Login with Fitbit</button>
        </div>
    );
};

export default LoginForm;