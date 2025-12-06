import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

const USERS_KEY = "resumeai_users";
const SCANS_PREFIX = "resumeai_scans_";

function AdminDashboard() {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const raw = localStorage.getItem(USERS_KEY);
    if (!raw) {
      setUsers([]);
      return;
    }
    try {
      const parsed = JSON.parse(raw);
      setUsers(parsed);
    } catch {
      setUsers([]);
    }
  }, []);

  const getScansForUser = (username) => {
    const key = SCANS_PREFIX + username;
    const raw = localStorage.getItem(key);
    if (!raw) return [];
    try {
      return JSON.parse(raw);
    } catch {
      return [];
    }
  };

  return (
    <section className="page-container">
      <div className="scanner-card" style={{ alignItems: "stretch" }}>
        <h2 className="scanner-title">Admin Dashboard</h2>
        <p className="scanner-subtitle">
          Signed in as <strong>{user?.name}</strong> ({user?.role}). View all
          registered accounts and their scan history in this browser.
        </p>

        {users.length === 0 && (
          <p style={{ marginTop: 12 }}>No registered users found.</p>
        )}

        {users.length > 0 && (
          <div style={{ marginTop: 16 }}>
            {users.map((u) => {
              const scans = getScansForUser(u.username);
              return (
                <div
                  key={u.id}
                  style={{
                    borderBottom: "1px solid #e5e7eb",
                    padding: "10px 0",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      marginBottom: 4,
                    }}
                  >
                    <div>
                      <strong>{u.name}</strong>{" "}
                      <span style={{ fontSize: 13, color: "#6b7280" }}>
                        (@{u.username})
                      </span>
                      <div style={{ fontSize: 13, color: "#4b5563" }}>
                        {u.email} · {u.role}
                      </div>
                    </div>
                    <div style={{ fontSize: 13, color: "#6b7280" }}>
                      {scans.length} scans
                    </div>
                  </div>

                  {scans.length > 0 && (
                    <ul className="breakdown-list">
                      {scans.map((scan) => (
                        <li key={scan.id} className="breakdown-item">
                          <span className="breakdown-label">
                            {scan.fileName || "Untitled resume"}
                          </span>
                          <span className="breakdown-points">
                            {scan.score}%
                          </span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}

export default AdminDashboard;
