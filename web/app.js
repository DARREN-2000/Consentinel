const output = document.getElementById("output");
const apiBaseInput = document.getElementById("apiBase");

const DEFAULT_API_BASE = "http://localhost:8000/api";
const API_BASE_KEY = "relevance_engine_api_base";

function getApiBase() {
  return (localStorage.getItem(API_BASE_KEY) || DEFAULT_API_BASE).replace(/\/$/, "");
}

function setOutput(value) {
  output.textContent =
    typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

async function callApi(path, options = {}) {
  const response = await fetch(`${getApiBase()}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  const payload = await response.json().catch(() => ({ detail: "No JSON response" }));

  if (!response.ok) {
    throw new Error(JSON.stringify(payload));
  }

  return payload;
}

function bindForm(formId, path, transform) {
  const form = document.getElementById(formId);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const raw = Object.fromEntries(formData.entries());
    const body = transform ? transform(raw) : raw;

    try {
      const result = await callApi(path, {
        method: "POST",
        body: JSON.stringify(body),
      });
      setOutput(result);
    } catch (error) {
      setOutput(`Request failed: ${error.message}`);
    }
  });
}

apiBaseInput.value = getApiBase();

document.getElementById("saveApiBase").addEventListener("click", () => {
  const value = apiBaseInput.value.trim() || DEFAULT_API_BASE;
  localStorage.setItem(API_BASE_KEY, value);
  setOutput(`Saved API base URL: ${getApiBase()}`);
});

document.getElementById("healthBtn").addEventListener("click", async () => {
  try {
    const result = await callApi("/health", { method: "GET" });
    setOutput(result);
  } catch (error) {
    setOutput(`Request failed: ${error.message}`);
  }
});

bindForm("userForm", "/users");
bindForm("consentForm", "/consents");
bindForm("eventForm", "/events");
bindForm("nbaForm", "/decisions/next-best-action", (raw) => ({ user_id: raw.user_id }));
