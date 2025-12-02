import React from "react";

function Contact() {
  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Thanks for reaching out! This demo doesn't send messages yet, but your form is working.");
  };

  return (
    <section className="page-container contact-page">
      <div className="contact-hero">
        <h1 className="contact-title">Get in touch</h1>
        <p className="contact-subtitle">
          Have a question, feature idea, or want help understanding your
          resume score? Reach out and we’ll get back to you as soon as we can.
        </p>
      </div>

      <div className="contact-grid">
        <div className="contact-card">
          <h3>General questions</h3>
          <p>
            Ask anything about how ResumeAI works, how we score, or how to get the
            best results from your resume.
          </p>
          <p className="contact-card-email">support@resumeai.com</p>
        </div>
        <div className="contact-card">
          <h3>Feedback & ideas</h3>
          <p>
            Found a bug, have a feature request, or want a new type of analysis?
            We’d love to hear from you.
          </p>
          <p className="contact-card-email">feedback@resumeai.com</p>
        </div>
        <div className="contact-card">
          <h3>Collabs & projects</h3>
          <p>
            Working on a portfolio, school project, or hackathon and want to use
            ResumeAI? Reach out and let’s talk.
          </p>
          <p className="contact-card-email">projects@resumeai.com</p>
        </div>
      </div>


      <div className="contact-layout">
        <div className="contact-info">
          <h2>Send us a message</h2>
          <p>
            Fill out the form and let us know what you’re working on. The more
            context you share about your resume, goals, and roles you’re targeting,
            the better we can help.
          </p>

          <ul className="contact-list">
            <li>💬 Ask about your resume score and how to improve it.</li>
            <li>🧠 Share ideas for new checks or analysis we should add.</li>
            <li>🤝 Talk about using ResumeAI in a class, club, or project.</li>
          </ul>
        </div>

        <div className="contact-form-card">
          <form onSubmit={handleSubmit} className="contact-form">
            <div className="contact-form-row">
              <div className="contact-field">
                <label htmlFor="name">Name</label>
                <input
                  id="name"
                  type="text"
                  placeholder="Your name"
                  className="contact-input"
                  required
                />
              </div>
              <div className="contact-field">
                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  className="contact-input"
                  required
                />
              </div>
            </div>

            <div className="contact-field">
              <label htmlFor="topic">What can we help with?</label>
              <select id="topic" className="contact-input">
                <option>Understanding my score</option>
                <option>Improving my resume</option>
                <option>Feature request</option>
                <option>Bug or issue</option>
                <option>Collaboration / project</option>
                <option>Other</option>
              </select>
            </div>

            <div className="contact-field">
              <label htmlFor="message">Message</label>
              <textarea
                id="message"
                rows="4"
                placeholder="Share a bit about your resume, goals, or what you’d like help with."
                className="contact-input contact-textarea"
                required
              />
            </div>

            <button type="submit" className="contact-btn">
              Send message
            </button>

            <p className="contact-footnote">
              We typically respond within 1–2 business days for most questions.
            </p>
          </form>
        </div>
      </div>
    </section>
  );
}

export default Contact;
