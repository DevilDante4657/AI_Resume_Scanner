import React, { useState } from "react";

function Scanner() {
  const [file, setFile] = useState(null);
  const [score, setScore] = useState(null);
  const [breakdown, setBreakdown] = useState([]);
  const [summary, setSummary] = useState("");

  const extractText = (file) =>
    new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result || "");
      reader.readAsText(file);
    });

  const analyzeResume = (text) => {
    const lower = text.toLowerCase();
    let total = 0;
    const items = [];

    const addCheck = (label, met, points) => {
      if (met) total += points;
      items.push({ label, met, points: met ? points : 0 });
    };

    // 1. Sections
    addCheck(
      "Has Experience / Work Experience section",
      lower.includes("experience"),
      20
    );

    addCheck("Has Education section", lower.includes("education"), 15);

    addCheck("Has Skills / Technical Skills section", lower.includes("skills"), 15);

    addCheck("Has Projects section", lower.includes("projects"), 10);

    // 2. Contact info
    const hasEmail = /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i.test(text);
    addCheck("Contains an email address", hasEmail, 10);

    const hasPhone =
      /\b(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b/.test(text);
    addCheck("Contains a phone number", hasPhone, 5);

    // 3. Bullets & action verbs
    const lines = text.split(/\r?\n/);
    const bulletLines = lines.filter((line) =>
      line.trim().match(/^[-*•]/)
    );
    addCheck(
      "Uses bullet points for responsibilities/achievements",
      bulletLines.length >= 5,
      10
    );

    const actionVerbs = [
      "developed",
      "implemented",
      "led",
      "created",
      "built",
      "designed",
      "managed",
      "improved",
      "achieved",
      "optimized",
      "analyzed",
      "collaborated",
    ];

    const bulletWithActionVerb = bulletLines.some((line) => {
      const firstWord = line
        .replace(/^[-*•]\s*/, "")
        .trim()
        .split(" ")[0]
        .toLowerCase();
      return actionVerbs.includes(firstWord);
    });

    addCheck(
      "Bullets start with strong action verbs",
      bulletWithActionVerb,
      5
    );

    // 4. Length
    const length = text.length;
    const goodLength = length >= 800 && length <= 8000; // ~1–2 pages
    addCheck(
      "Reasonable resume length (not too short/long)",
      goodLength,
      10
    );

    const finalScore = Math.max(0, Math.min(100, total));

    let summaryText = "";
    if (finalScore >= 85) {
      summaryText =
        "Strong resume. Mostly well-structured with good sections and details.";
    } else if (finalScore >= 70) {
      summaryText =
        "Solid base. Improving structure, bullets, and missing sections will help.";
    } else if (finalScore >= 55) {
      summaryText =
        "Average resume. Add missing sections and more detailed bullet points.";
    } else {
      summaryText =
        "Weak structure. You may be missing sections like Experience, Skills, or Education.";
    }

    return { score: finalScore, breakdown: items, summary: summaryText };
  };

  const handleUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    if (!uploadedFile) return;

    setFile(uploadedFile);

    const text = await extractText(uploadedFile);
    const { score, breakdown, summary } = analyzeResume(text);

    setScore(score);
    setBreakdown(breakdown);
    setSummary(summary);
  };

  return (
    <section className="page-container scanner-page">
      <div className="scanner-card">
        <h2 className="scanner-title">Resume Scanner</h2>
        <p className="scanner-subtitle">
          Upload your resume to get a quick structural score and a breakdown of
          what’s strong and what’s missing.
        </p>

        <label className="upload-box">
          <div className="upload-inner">
            <div className="upload-icon">⬆️</div>
            <div className="upload-text-main">
              {file ? file.name : "Click to upload your resume"}
            </div>
            <div className="upload-text-sub">
              .txt works best · You can export from Word/Google Docs as plain text
            </div>
          </div>
          <input
            type="file"
            accept=".txt,.md,.rtf,.docx,.pdf"
            style={{ display: "none" }}
            onChange={handleUpload}
          />
        </label>

        {score !== null && (
          <div className="result-box">
            <div className="score-row">
              <div>
                <div className="score-label">Overall score</div>
                <div className="score">{score}%</div>
              </div>
              <div className="score-pill">
                {score >= 85
                  ? "Great"
                  : score >= 70
                  ? "Good"
                  : score >= 55
                  ? "Okay"
                  : "Needs work"}
              </div>
            </div>

            <p className="scanner-summary">{summary}</p>

            <h3 className="breakdown-heading">What we checked</h3>
            <ul className="breakdown-list">
              {breakdown.map((item, idx) => (
                <li
                  key={idx}
                  className={`breakdown-item ${
                    item.met ? "met" : "not-met"
                  }`}
                >
                  <span className="breakdown-label">{item.label}</span>
                  <span className="breakdown-points">
                    {item.met ? `+${item.points}` : "+0"}
                  </span>
                </li>
              ))}
            </ul>

            <button className="download-btn">
              Download report (coming soon)
            </button>
          </div>
        )}
      </div>
    </section>
  );
}

export default Scanner;
