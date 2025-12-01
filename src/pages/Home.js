import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home-container">
      {/* HERO SECTION */}
      <section className="hero">
        <div className="hero-inner">
          {/* Left side text */}
          <div className="hero-left">
            <p className="hero-kicker">AI-powered resume insights</p>
            <h1 className="hero-title">Make your resume recruiter-ready.</h1>
            <p className="hero-subtitle">
              ResumeAI scans your resume in seconds, checks key sections,
              and gives you a clear score with specific, actionable feedback.
            </p>

            <div className="hero-cta-row">
              <Link to="/scanner">
                <button className="primary-btn hero-primary-btn">
                  Scan my resume
                </button>
              </Link>
              <p className="hero-secondary">No account needed · Free to try</p>
            </div>

            <div className="hero-metric-row">
              <div className="hero-metric">
                <span className="hero-metric-number">60s</span>
                <span className="hero-metric-label">average review time</span>
              </div>
              <div className="hero-metric">
                <span className="hero-metric-number">4+</span>
                <span className="hero-metric-label">key sections analyzed</span>
              </div>
            </div>
          </div>

          {/* Right side preview card */}
          <div className="hero-right">
            <div className="hero-card">
              <div className="hero-card-header">
                <span className="hero-card-title">Sample scan</span>
                <span className="hero-card-pill">Product Manager</span>
              </div>

              <div className="hero-score-row">
                <div className="hero-score">82%</div>
                <div className="hero-score-text">
                  <p className="hero-score-label">Overall score</p>
                  <p className="hero-score-sub">
                    Strong structure with room to improve bullet points.
                  </p>
                </div>
              </div>

              <ul className="hero-card-list">
                <li>✓ Experience & Education sections detected</li>
                <li>✓ Clear skills section with technical stack</li>
                <li>○ Few weak bullet points without action verbs</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section className="home-section">
        <h2 className="home-section-title">Why ResumeAI?</h2>
        <p className="home-section-subtitle">
          Built for students and early-career professionals who want quick, 
          honest feedback without overcomplicated tools.
        </p>

        <div className="home-feature-grid">
          <div className="feature-card">
            <h3>Structural scoring</h3>
            <p>
              We check for must-have sections like Experience, Education,
              Skills, and Projects so nothing important is missing.
            </p>
          </div>
          <div className="feature-card">
            <h3>Action-based feedback</h3>
            <p>
              Highlights weak bullet points and suggests where you need stronger
              action verbs and quantifiable results.
            </p>
          </div>
          <div className="feature-card">
            <h3>Instant results</h3>
            <p>
              Upload your resume and get a score and breakdown in under a
              minute—no sign up, no friction.
            </p>
          </div>
          <div className="feature-card">
            <h3>Private & local</h3>
            <p>
              Your file is analyzed directly in the browser and never shown
              publicly. Perfect for job hunts and internship season.
            </p>
          </div>
        </div>
      </section>

      {/* TESTIMONIAL / CTA SECTION */}
      <section className="home-section home-section-alt">
        <div className="home-testimonial">
          <p className="testimonial-quote">
            “ResumeAI made it obvious what my resume was missing. After a few
            tweaks, I started getting way more callbacks.”
          </p>
          <p className="testimonial-author">— Early-career Software Engineer</p>
        </div>

        <div className="home-cta-band">
          <div>
            <h3>Ready to see how your resume scores?</h3>
            <p>Upload a file and get feedback in less than a minute.</p>
          </div>
          <Link to="/scanner">
            <button className="primary-btn">Start scanning</button>
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Home;
