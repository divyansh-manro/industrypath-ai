// frontend/script.js

const btn = document.getElementById("submitBtn");
const ideaInput = document.getElementById("idea");
const resultDiv = document.getElementById("result");

const BACKEND_PROD_URL = "https://industrypath-backend.onrender.com";

const BASE_URL =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"           // local dev
    : BACKEND_PROD_URL;                 // production

btn.addEventListener("click", async () => {
  const idea = ideaInput.value.trim();
  if (!idea) {
    alert("Please enter an idea first.");
    return;
  }

  resultDiv.classList.remove("empty-state");
  resultDiv.innerHTML = "<em>Thinking...</em>";

  try {
    const res = await fetch(`${BASE_URL}/api/generate-roadmap`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ idea }),
    });

    if (!res.ok) {
      throw new Error("Server error");
    }

    const data = await res.json();
    renderResult(data);
  } catch (err) {
    console.error(err);
    resultDiv.innerHTML =
      "<span style='color:red'>Error generating roadmap. Check the backend logs.</span>";
  }
});

function renderResult(data) {
  const parsed = data.parsed && typeof data.parsed === "object" ? data.parsed : null;

  if (!parsed) {
    const raw = (data.raw_text || "").trim();
    const cleaned = raw.replace(/```json|```/g, "");
    resultDiv.innerHTML = `
      <div class="result-section">
        <h3>Raw Output</h3>
        <div class="mono-block">${escapeHtml(cleaned)}</div>
      </div>
    `;
    return;
  }

  let html = "";

  if (parsed.refined_goal) {
    html += `
      <div class="result-section">
        <h3>Refined Goal</h3>
        <p>${escapeHtml(parsed.refined_goal)}</p>
      </div>
    `;
  }

  if (Array.isArray(parsed.keywords) && parsed.keywords.length > 0) {
    html += `
      <div class="result-section">
        <h3>Keywords</h3>
        <div class="pill-row">
          ${parsed.keywords
            .map((kw) => `<span class="pill">${escapeHtml(kw)}</span>`)
            .join("")}
        </div>
      </div>
    `;
  }

  if (parsed.project_topic) {
    html += `
      <div class="result-section">
        <h3>Project Topic</h3>
        <p>${escapeHtml(parsed.project_topic)}</p>
      </div>
    `;
  }

  if (Array.isArray(parsed.learning_roadmap) && parsed.learning_roadmap.length > 0) {
    html += `
      <div class="result-section">
        <h3>Learning Roadmap</h3>
        <ul class="roadmap-list">
          ${parsed.learning_roadmap
            .map((step) => {
              const title = step.title || "Step";
              const desc = step.description || "";
              return `
                <li class="roadmap-item">
                  <div class="roadmap-dot"></div>
                  <div>
                    <div class="roadmap-title">${escapeHtml(title)}</div>
                    <div class="roadmap-desc">${escapeHtml(desc)}</div>
                  </div>
                </li>
              `;
            })
            .join("")}
        </ul>
      </div>
    `;
  }

  if (Array.isArray(parsed.companies) && parsed.companies.length > 0) {
    html += `
      <div class="result-section">
        <h3>Companies</h3>
        <div class="grid-3">
          ${parsed.companies
            .map((c) => {
              const note = c.short_note || "";
              return `
                <div class="mini-card">
                  <div class="mini-title">
                    <a href="${c.url}" target="_blank" rel="noopener noreferrer">
                      ${escapeHtml(c.name)}
                    </a>
                  </div>
                  <div class="mini-sub">${escapeHtml(note)}</div>
                </div>
              `;
            })
            .join("")}
        </div>
      </div>
    `;
  }

  if (Array.isArray(parsed.communities) && parsed.communities.length > 0) {
    html += `
      <div class="result-section">
        <h3>Communities</h3>
        <div class="grid-3">
          ${parsed.communities
            .map((c) => {
              const why = c.why_relevant || "";
              return `
                <div class="mini-card">
                  <div class="mini-title">
                    <a href="${c.url}" target="_blank" rel="noopener noreferrer">
                      ${escapeHtml(c.name)}
                    </a>
                  </div>
                  <div class="mini-sub">${escapeHtml(why)}</div>
                </div>
              `;
            })
            .join("")}
        </div>
      </div>
    `;
  }

  if (Array.isArray(parsed.courses) && parsed.courses.length > 0) {
    html += `
      <div class="result-section">
        <h3>Courses & Resources</h3>
        <div class="grid-3">
          ${parsed.courses
            .map((c) => {
              const level = c.level || "";
              return `
                <div class="mini-card">
                  <div class="mini-title">
                    <a href="${c.url}" target="_blank" rel="noopener noreferrer">
                      ${escapeHtml(c.title)}
                    </a>
                  </div>
                  <div class="mini-sub">${escapeHtml(level)}</div>
                </div>
              `;
            })
            .join("")}
        </div>
      </div>
    `;
  }

  if (!html) {
    const raw = (data.raw_text || "").trim();
    const cleaned = raw.replace(/```json|```/g, "");
    html = `
      <div class="result-section">
        <h3>Raw Output</h3>
        <div class="mono-block">${escapeHtml(cleaned)}</div>
      </div>
    `;
  }

  resultDiv.innerHTML = html;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
