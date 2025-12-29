import { useState } from "react";
import api from "../api/axios";
import { useNavigate, Link } from "react-router-dom";

function Register() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Clear previous errors

    // Trim whitespace
    const trimmedUsername = username.trim();
    const trimmedEmail = email.trim();
    const trimmedPassword = password.trim();

    if (!trimmedUsername || !trimmedEmail || !trimmedPassword) {
      setError("All fields are required");
      return;
    }

    if (trimmedPassword.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(trimmedEmail)) {
      setError("Please enter a valid email address");
      return;
    }

    try {
      await api.post("/register", {
        username: trimmedUsername,
        email: trimmedEmail,
        password: trimmedPassword,
      });

      navigate("/login");
    } catch (error) {
      console.error("Registration error:", error);
      
      // Network error (server not reachable)
      if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
        setError(`Cannot connect to server. Make sure the backend is running on ${import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"}`);
        return;
      }
      
      // Request was made but no response (server down or CORS issue)
      if (!error.response) {
        setError("Server is not responding. Check if the backend server is running.");
        return;
      }
      
      // Server responded with error
      if (error.response?.data?.detail) {
        setError(error.response.data.detail);
      } else if (error.response?.data?.message) {
        setError(error.response.data.message);
      } else if (error.response?.status === 500) {
        setError("Server error. Please try again later.");
      } else if (error.response?.status === 400) {
        setError("Invalid data. Please check your input.");
      } else {
        setError(`Registration failed: ${error.message || "Unknown error"}`);
      }
    }
  };

  return (
    <div className="auth-container">
      <h2>Register</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          id="register-username"
          name="username"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          id="register-email"
          name="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          id="register-password"
          name="password"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">Register</button>
      </form>

      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}

export default Register;
