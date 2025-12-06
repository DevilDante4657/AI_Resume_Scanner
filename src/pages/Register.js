import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const USERS_KEY = "resumeai_users";

function Register() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
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

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!name || !username || !email || !password || !confirm) {
      setError("Please fill in all fields.");
      return;
    }

    if (/\s/.test(username)) {
      setError("Username cannot contain spaces.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }

    const users = getUsers();

    const usernameTaken = users.some(
      (u) => u.username.toLowerCase() === username.toLowerCase()
    );
    if (usernameTaken) {
      setError("That username is already taken.");
      return;
    }

    const emailTaken = users.some(
      (u) => u.email.toLowerCase() === email.toLowerCase()
    );
    if (emailTaken) {
      setError("An account with that email already exists.");
      return;
    }

    const newUser = {
      id: Date.now(),
      name: name.trim(),
      username: username.trim(),
      email: email.trim(),
      password, 
      role: "user",
    };

    const updatedUsers = [...users, newUser];
    saveUsers(updatedUsers);

    login(newUser);
    navigate("/scanner");
  };

  return (
    <section className="page-container login-page">
      <div className="login-card">
        <h1>Create an account</h1>
        <p className="login-subtitle">
          Sign up to start scanning resumes and save your history in this
          browser.
        </p>

        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="login-field">
            <label htmlFor="reg-name">Full name</label>
            <input
              id="reg-name"
              className="contact-input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
            />
          </div>

          <div className="login-field">
            <label htmlFor="reg-username">Username</label>
            <input
              id="reg-username"
              className="contact-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
            />
          </div>

          <div className="login-field">
            <label htmlFor="reg-email">Email</label>
            <input
              id="reg-email"
              className="contact-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              type="email"
              placeholder="you@example.com"
            />
          </div>

          <div className="login-field">
            <label htmlFor="reg-password">Password</label>
            <input
              id="reg-password"
              className="contact-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              placeholder="••••••••"
            />
          </div>

          <div className="login-field">
            <label htmlFor="reg-confirm">Confirm password</label>
            <input
              id="reg-confirm"
              className="contact-input"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              type="password"
              placeholder="••••••••"
            />
          </div>

          <button type="submit" className="primary-btn" style={{ width: "100%" }}>
            Create account
          </button>
        </form>

        <div className="login-toggle">
          <span>Already have an account? </span>
          <button type="button" onClick={() => navigate("/login")}>
            Sign in
          </button>
        </div>
      </div>
    </section>
  );
}

export default Register;
