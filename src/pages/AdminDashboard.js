import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

const USERS_KEY = "resumeai_users";
const SCANS_PREFIX = "resumeai_scans_";
const JOBS_PREFIX = "resumeai_jobs_";

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

  const getJobsForUser = (username) => {
    const key = JOBS_PREFIX + username;
    const raw = localStorage.getItem(key);
    if (!raw) return [];
    try {
      return JSON.parse(raw);
    } catch {
      return [];
    }
  };

  const handleDownload = (scan) => {
    if (!scan.content) {
      alert("No resume content stored for this scan (old entry or empty file).");
      return;
    }
    const blob = new Blob([scan.content], {
      type: "text/plain;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = scan.fileName || "resume.txt";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  return (
    <section className="page-container">
      <div className="scanner-card" style={{ alignItems: "stretch" }}>
        <h2 className="scanner-title">Admin Dashboard</h2>
        <p className="scanner-subtitle">
          Signed in as <strong>{user?.name}</strong> ({user?.role}). View all
          registered accounts, their resume scores, and the jobs they&apos;ve
          logged in this browser.
        </p>

        {users.length === 0 && (
          <p style={{ marginTop: 12 }}>No registered users found.</p>
        )}

        {users.length > 0 && (
          <div style={{ marginTop: 16 }}>
            {users.map((u) => {
              const scans = getScansForUser(u.username);
              const jobs = getJobsForUser(u.username);

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
                      <strong>{u.fullName || u.name || u.username}</strong>{" "}
                      <span style={{ fontSize: 13, color: "#6b7280" }}>
                        (@{u.username})
                      </span>
                      <div style={{ fontSize: 13, color: "#4b5563" }}>
                        {u.email} · {u.role}
                      </div>
                    </div>
                    <div
                      style={{
                        fontSize: 13,
                        color: "#6b7280",
                        textAlign: "right",
                      }}
                    >
                      {scans.length} scans
                      <br />
                      {jobs.length} jobs logged
                    </div>
                  </div>


                  {scans.length > 0 && (
                    <>
                      <div
                        style={{
                          fontSize: 13,
                          color: "#6b7280",
                          marginBottom: 4,
                        }}
                      >
                        Resumes
                      </div>
                      <ul className="breakdown-list">
                        {scans.map((scan) => (
                          <li key={scan.id} className="breakdown-item">
                            <span className="breakdown-label">
                              {scan.fileName || "Untitled resume"}
                            </span>
                            <span className="breakdown-points">
                              {scan.score}%
                              <button
                                type="button"
                                className="link-button"
                                onClick={() => handleDownload(scan)}
                                style={{ marginLeft: 8 }}
                              >
                                Download
                              </button>
                            </span>
                          </li>
                        ))}
                      </ul>
                    </>
                  )}

                  {/* Jobs list */}
                  {jobs.length > 0 && (
                    <>
                      <div
                        style={{
                          fontSize: 13,
                          color: "#6b7280",
                          margin: "6px 0 4px",
                        }}
                      >
                        Jobs applied to
                      </div>
                      <ul className="breakdown-list">
                        {jobs.map((job) => (
                          <li key={job.id} className="breakdown-item">
                            <span className="breakdown-label">
                              {job.title}
                              {job.company ? ` · ${job.company}` : ""}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </>
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
