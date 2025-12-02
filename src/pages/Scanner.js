import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

const STORAGE_PREFIX = "resumeai_scans_";

function Scanner() {
  const { user } = useAuth();
  const [file, setFile] = useState(null);
  const [score, setScore] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");


  useEffect(() => {
    if (!user || !user.username) return;
    const key = STORAGE_PREFIX + user.username;
    const saved = localStorage.getItem(key);
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch {
        setHistory([]);
      }
    }
  }, [user]);


  const extractText = (file) =>
    new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result || "");
      reader.readAsText(file);
    });

 
  const analyzeResume = (text) => {
  
    const length = text.length;
    let score = Math.min(100, Math.max(5, Math.floor(length / 100)));
    return score;
  };

  const saveHistory = (entry) => {
    if (!user || !user.username) return;
    const key = STORAGE_PREFIX + user.username;
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

    const text = await extractText(uploaded);
    const finalScore = analyzeResume(text);

    setScore(finalScore);

    saveHistory({
      id: Date.now(),
      fileName: uploaded.name,
      score: finalScore,
      createdAt: new Date().toISOString(),
    });
  };

  return (
    <section className="page-container scanner-page">
      <div className="scanner-card">
        <h2 className="scanner-title">Resume Scanner</h2>

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
      </div>
    </section>
  );
}

export default Scanner;
