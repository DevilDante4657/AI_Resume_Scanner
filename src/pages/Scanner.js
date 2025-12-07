// src/pages/Scanner.js
import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

const SCANS_PREFIX = "resumeai_scans_";
const JOBS_PREFIX = "resumeai_jobs_";

function Scanner() {
  const { user } = useAuth();
  const [file, setFile] = useState(null);
  const [score, setScore] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  // Jobs state
  const [jobs, setJobs] = useState([]);
  const [jobTitle, setJobTitle] = useState("");
  const [jobCompany, setJobCompany] = useState("");

  // Load scans + jobs for this user
  useEffect(() => {
    if (!user || !user.username || user.role === "admin") return;

    const scanKey = SCANS_PREFIX + user.username;
    const jobsKey = JOBS_PREFIX + user.username;

    const savedScans = localStorage.getItem(scanKey);
    if (savedScans) {
      try {
        setHistory(JSON.parse(savedScans));
      } catch {
        setHistory([]);
      }
    }

    const savedJobs = localStorage.getItem(jobsKey);
    if (savedJobs) {
      try {
        setJobs(JSON.parse(savedJobs));
      } catch {
        setJobs([]);
      }
    }
  }, [user]);

  const extractText = (file) =>
    new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result || "");
      reader.readAsText(file);
    });

  // SIMPLE scoring placeholder (backend team will replace)
  const analyzeResume = (text) => {
    const length = text.length;
    let score = Math.min(100, Math.max(5, Math.floor(length / 100)));
    return score;
  };

  const saveHistory = (entry) => {
    if (!user || !user.username || user.role === "admin") return;

    const key = SCANS_PREFIX + user.username;
    const updated = [entry, ...history].slice(0, 10);
    setHistory(updated);
    localStorage.setItem(key, JSON.stringify(updated));
  };

  const handleUpload = async (e) => {
  const uploaded = e.target.files[0];
  if (!uploaded) return;

  if (!user || !user.username) {
    setError("You must be logged in.");
    return;
  }

  setFile(uploaded);
  setError("");

  const text = await extractText(uploaded);  // ⬅️ this reads the resume
  const finalScore = analyzeResume(text);

  setScore(finalScore);

  // ⬅️ THIS PART IS IMPORTANT
  saveHistory({
    id: Date.now(),
    fileName: uploaded.name,
    score: finalScore,
    createdAt: new Date().toISOString(),
    content: text,           // ⬅️ this line MUST exist
  });
};

  // ----- Jobs Applied section -----
  const saveJobs = (updatedJobs) => {
    if (!user || !user.username || user.role === "admin") return;

    const key = JOBS_PREFIX + user.username;
    setJobs(updatedJobs);
    localStorage.setItem(key, JSON.stringify(updatedJobs));
  };

  const handleAddJob = (e) => {
    e.preventDefault();
    if (!jobTitle.trim() && !jobCompany.trim()) return;

    const newJob = {
      id: Date.now(),
      title: jobTitle.trim() || "Untitled role",
      company: jobCompany.trim(),
      createdAt: new Date().toISOString(),
    };

    const updated = [newJob, ...jobs];
    saveJobs(updated);

    setJobTitle("");
    setJobCompany("");
  };

  return (
    <section className="page-container scanner-page">
      <div className="scanner-card">
        <h2 className="scanner-title">Resume Scanner</h2>

        {/* Upload + Score */}
        <label className="upload-box">
          <div className="upload-inner">
            <div className="upload-icon">⬆️</div>
            <div className="upload-text-main">
              {file ? file.name : "Click to upload your resume"}
            </div>
            <div className="upload-text-sub">.txt works best</div>
          </div>
          <input
            type="file"
            accept=".txt,.md,.rtf,.docx,.pdf"
            style={{ display: "none" }}
            onChange={handleUpload}
          />
        </label>

        {error && (
          <div className="login-error" style={{ marginTop: 10 }}>
            {error}
          </div>
        )}

        {score !== null && (
          <div className="result-box" style={{ textAlign: "center" }}>
            <div style={{ fontSize: "16px", color: "#6b7280" }}>Score</div>
            <div
              style={{
                fontSize: "60px",
                fontWeight: "700",
                color: "#7C3AED",
                marginTop: "-5px",
              }}
            >
              {score}%
            </div>
          </div>
        )}

        {history.length > 0 && (
          <div className="result-box" style={{ marginTop: 20 }}>
            <h3 className="breakdown-heading">Recent scans</h3>
            <ul className="breakdown-list">
              {history.map((scan) => (
                <li key={scan.id} className="breakdown-item">
                  <span className="breakdown-label">{scan.fileName}</span>
                  <span className="breakdown-points">{scan.score}%</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Jobs Applied Section */}
        {user?.role !== "admin" && (
          <div className="result-box" style={{ marginTop: 20 }}>
            <h3 className="breakdown-heading">Jobs you've applied to</h3>

            <form onSubmit={handleAddJob} className="jobs-form">
              <div className="jobs-row">
                <input
                  className="contact-input"
                  placeholder="Job title (e.g. Software Engineer)"
                  value={jobTitle}
                  onChange={(e) => setJobTitle(e.target.value)}
                />
              </div>

              <div className="jobs-row">
                <input
                  className="contact-input"
                  placeholder="Company (e.g. Amazon, Epic, Google)"
                  value={jobCompany}
                  onChange={(e) => setJobCompany(e.target.value)}
                />
              </div>

              <button type="submit" className="primary-btn jobs-add-btn">
                Add job
              </button>
            </form>

            {jobs.length > 0 && (
              <ul className="breakdown-list" style={{ marginTop: 12 }}>
                {jobs.map((job) => (
                  <li key={job.id} className="breakdown-item">
                    <span className="breakdown-label">
                      {job.title}
                      {job.company ? ` · ${job.company}` : ""}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </section>
  );
}

export default Scanner;
