import React from "react";
import { Link } from "react-router-dom";

function About() {
  return (
    <section className="page-container about-page">

      <div className="about-hero">
        <h1 className="about-title">Why we built ResumeAI</h1>
        <p className="about-subtitle">
          ResumeAI was created for students and early-career professionals who
          are tired of guessing whether their resume is actually ready. Instead
          of generic templates, we focus on clear structure, key sections, and
          honest, instant feedback.
        </p>

        <div className="about-badges">
          <div className="about-badge">
            <span className="about-badge-label">Built for students</span>
            <span className="about-badge-text">
              Designed around internships, new grads, and junior roles.
            </span>
          </div>
          <div className="about-badge">
            <span className="about-badge-label">Fast & practical</span>
            <span className="about-badge-text">
              Score, breakdown, and next steps in under a minute.
            </span>
          </div>
          <div className="about-badge">
            <span className="about-badge-label">Private by default</span>
            <span className="about-badge-text">
              Your resume is analyzed locally in the browser.
            </span>
          </div>
        </div>
      </div>


      <div className="about-grid">

        <div className="about-card">
          <h2 className="about-card-title">How ResumeAI works</h2>
          <ol className="about-steps">
            <li>
              <span className="about-step-number">1</span>
              <div className="about-step-content">
                <h3>Upload your resume</h3>
                <p>
                  Start with a simple .txt export from Word, Google Docs, or
                  your favorite editor.
                </p>
              </div>
            </li>
            <li>
              <span className="about-step-number">2</span>
              <div className="about-step-content">
                <h3>We analyze key structure</h3>
                <p>
                  We look for core sections like Experience, Education, Skills,
                  and Projects, plus contact info and bullet quality.
                </p>
              </div>
            </li>
            <li>
              <span className="about-step-number">3</span>
              <div className="about-step-content">
                <h3>Get a score & breakdown</h3>
                <p>
                  You’ll see a simple score out of 100 and a checklist of what
                  you’re doing well and what you’re missing.
                </p>
              </div>
            </li>
          </ol>
        </div>


        <div className="about-card">
          <h2 className="about-card-title">Our philosophy</h2>
          <ul className="about-list">
            <li>
              <strong>Clarity over hype.</strong> We don’t promise “perfect”
              resumes—just clear, honest signals on how to improve.
            </li>
            <li>
              <strong>Less friction.</strong> No accounts, no onboarding
              tunnel. Open the site, upload, get feedback.
            </li>
            <li>
              <strong>Student-first.</strong> We care about resumes that list
              projects, coursework, and early experience—not just senior titles.
            </li>
            <li>
              <strong>Respect for your data.</strong> Your resume is your
              story. We treat it that way and keep it local to your browser.
            </li>
          </ul>
        </div>
      </div>


      <div className="about-cta">
        <div>
          <h2>Where we’re going next</h2>
          <p>
            We’re working toward deeper feedback—things like phrasing strength,
            impact language, and tailored suggestions for technical roles.
          </p>
        </div>
        <Link to="/scanner">
          <button className="primary-btn">Try the scanner</button>
        </Link>
      </div>
    </section>
  );
}

export default About;
