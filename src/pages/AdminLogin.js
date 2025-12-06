import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const USERS_KEY = "resumeai_users";

function AdminLogin() {
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

  const saveUsers = (users) => {
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
  };

  
  useEffect(() => {
    const users = getUsers();
    const hasAdmin = users.some((u) => u.role === "admin");

    if (!hasAdmin) {
      const adminUser = {
        id: Date.now(),
        name: "Admin",
        username: "admin",
        email: "admin@resumeai.com",
        password: "admin123",
        role: "admin",
      };
      saveUsers([...users, adminUser]);
    }
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!username || !password) {
      setError("Please enter username and password.");
      return;
    }

    const users = getUsers();


    const admin = users.find(
      (u) =>
        u.role === "admin" &&
        u.username.toLowerCase() === username.toLowerCase()
    );

    if (!admin || admin.password !== password) {
      setError("Invalid admin credentials.");
      return;
    }

    login(admin);
    navigate("/admin");
  };

  return (
    <section className="page-container login-page">
      <div className="login-card">
        <h1>Admin Login</h1>
        <p className="login-subtitle">Sign in to access the admin dashboard.</p>

        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="login-field">
            <label htmlFor="admin-username">Username</label>
            <input
              id="admin-username"
              className="contact-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
            />
          </div>

          <div className="login-field">
            <label htmlFor="admin-password">Password</label>
            <input
              id="admin-password"
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
          <span>Back to user login? </span>
          <button type="button" onClick={() => navigate("/login")}>
            Go to login
          </button>
        </div>
      </div>
    </section>
  );
}

export default AdminLogin;
