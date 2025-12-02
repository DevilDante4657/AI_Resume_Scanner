import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const USERS_KEY = "resumeai_users";

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const getUsers = () => {
    const raw = localStorage.getItem(USERS_KEY);
    if (!raw) return [];
    try {
      return JSON.parse(raw);
    } catch {
      return [];
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!username || !password) {
      setError("Please enter your username and password.");
      return;
    }

    const users = getUsers();
    const found = users.find(
      (u) => u.username.toLowerCase() === username.toLowerCase()
    );

    if (!found || found.password !== password) {
      setError("Invalid username or password.");
      return;
    }


    login(found);
    navigate("/scanner");
  };

  return (
    <section className="page-container login-page">
      <div className="login-card">
        <h1>Sign in</h1>
        <p className="login-subtitle">
          Enter your username and password to access your scans.
        </p>

        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="login-field">
            <label htmlFor="login-username">Username</label>
            <input
              id="login-username"
              className="contact-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
            />
          </div>

          <div className="login-field">
            <label htmlFor="login-password">Password</label>
            <input
              id="login-password"
              className="contact-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              placeholder="••••••••"
            />
          </div>

          <button type="submit" className="primary-btn" style={{ width: "100%" }}>
            Sign in
          </button>
        </form>

        <div className="login-toggle">
          <span>Don’t have an account? </span>
          <button type="button" onClick={() => navigate("/register")}>
            Register
          </button>
        </div>

        <div className="login-toggle" style={{ marginTop: 6 }}>
          <span>Admin? </span>
          <button type="button" onClick={() => navigate("/admin-login")}>
            Go to admin login
          </button>
        </div>
      </div>
    </section>
  );
}

export default Login;
