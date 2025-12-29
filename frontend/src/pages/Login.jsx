import { useState } from "react";
import api from "../api/axios";
import { setToken } from "../auth/auth";
import { useNavigate, Link } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/login", { username, password });
      setToken(res.data.access_token);
      navigate("/");
    } catch (error) {
      if (error.response?.data?.detail) {
        setError(error.response.data.detail);
      } else {
        setError("Invalid credentials");
      }
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          id="login-username"
          name="username"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          id="login-password"
          name="password"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">Login</button>
      </form>

      {/* ✅ THIS WAS MISSING */}
      <p style={{ marginTop: "10px" }}>
        Don’t have an account?{" "}
        <Link to="/register">Register</Link>
      </p>
    </div>
  );
}

export default Login;
