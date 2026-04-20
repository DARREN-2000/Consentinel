const output = document.getElementById("output");
const apiBaseInput = document.getElementById("apiBase");
const statusBadge = document.getElementById("statusBadge");
const latencyBadge = document.getElementById("latencyBadge");

const DEFAULT_API_BASE = "http://localhost:8000/api";
const API_BASE_KEY = "relevance_engine_api_base";
const LAST_USER_ID_KEY = "relevance_engine_last_user_id";
const REQUEST_TIMEOUT_MS = 15000;

function setStatus(type, text) {
  statusBadge.className = `badge ${type}`;
  statusBadge.textContent = text;
}

function setLatency(ms = null) {
  latencyBadge.textContent = ms == null ? "—" : `${ms} ms`;
}

function setOutput(value) {
  output.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

function getStoredApiBase() {
  return localStorage.getItem(API_BASE_KEY) || DEFAULT_API_BASE;
}

function normalizeApiBase(url) {
  const normalized = String(url || "").trim().replace(/\/$/, "");
  if (!normalized) {
    throw new Error("API base URL cannot be empty");
  }

  let parsed;
  try {
    parsed = new URL(normalized);
  } catch {
    throw new Error("API base URL is invalid");
  }

  if (!parsed.pathname.endsWith("/api")) {
    throw new Error("API base URL must end with /api");
  }

  return normalized;
}

function getApiBase() {
  return normalizeApiBase(getStoredApiBase());
}

function saveApiBase() {
  const normalized = normalizeApiBase(apiBaseInput.value || DEFAULT_API_BASE);
  localStorage.setItem(API_BASE_KEY, normalized);
  apiBaseInput.value = normalized;
  setOutput(`Saved API base URL: ${normalized}`);
}

function setAllButtonsDisabled(disabled) {
  document.querySelectorAll("button").forEach((button) => {
    button.disabled = disabled;
  });
}

function getLastUserId() {
  return localStorage.getItem(LAST_USER_ID_KEY) || "";
}

function saveLastUserId(userId) {
  if (!userId) return;
  localStorage.setItem(LAST_USER_ID_KEY, userId);
  document.querySelectorAll("[data-user-id-input]").forEach((input) => {
    if (!input.value) {
      input.value = userId;
    }
  });
}

async function callApi(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  const startedAt = performance.now();
  setStatus("loading", "Request in progress");
  setAllButtonsDisabled(true);

  try {
    const response = await fetch(`${getApiBase()}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
      signal: controller.signal,
    });

    const payload = await response
      .json()
      .catch(() => ({ detail: "Response body is not valid JSON" }));

    const durationMs = Math.round(performance.now() - startedAt);
    setLatency(durationMs);

    if (!response.ok) {
      setStatus("error", `Error ${response.status}`);
      throw new Error(JSON.stringify(payload));
    }

    setStatus("success", `Success ${response.status}`);
    return payload;
  } catch (error) {
    if (error.name === "AbortError") {
      setStatus("error", "Request timeout");
      throw new Error(`Request timed out after ${REQUEST_TIMEOUT_MS / 1000}s`);
    }

    setStatus("error", "Request failed");
    throw error;
  } finally {
    clearTimeout(timeout);
    setAllButtonsDisabled(false);
  }
}

function bindForm(formId, path, transform, onSuccess) {
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
      if (onSuccess) {
        onSuccess(result, raw);
      }
    } catch (error) {
      setOutput(`Request failed: ${error.message}`);
    }
  });
}

function hydrateApiAndUserId() {
  apiBaseInput.value = getStoredApiBase();
  const lastUserId = getLastUserId();
  if (!lastUserId) return;

  document.querySelectorAll("[data-user-id-input]").forEach((input) => {
    input.value = lastUserId;
  });
}

function bindControls() {
  document.getElementById("saveApiBase").addEventListener("click", () => {
    try {
      saveApiBase();
      setStatus("success", "API URL saved");
    } catch (error) {
      setStatus("error", "Invalid API URL");
      setOutput(`Configuration error: ${error.message}`);
    }
  });

  document.getElementById("healthBtn").addEventListener("click", async () => {
    try {
      const result = await callApi("/health", { method: "GET" });
      setOutput(result);
    } catch (error) {
      setOutput(`Request failed: ${error.message}`);
    }
  });

  document.getElementById("copyOutput").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(output.textContent || "");
      setStatus("success", "Output copied");
    } catch {
      setStatus("error", "Copy failed");
    }
  });

  document.getElementById("clearOutput").addEventListener("click", () => {
    setOutput("Ready.");
    setStatus("idle", "Idle");
    setLatency();
  });
}

bindForm("userForm", "/users", null, (result) => {
  saveLastUserId(result.id);
});
bindForm("consentForm", "/consents", null, (_result, raw) => {
  saveLastUserId(raw.user_id);
});
bindForm("eventForm", "/events", null, (_result, raw) => {
  saveLastUserId(raw.user_id);
});
bindForm("nbaForm", "/decisions/next-best-action", (raw) => ({ user_id: raw.user_id }),
  (_result, raw) => {
    saveLastUserId(raw.user_id);
  }
);

hydrateApiAndUserId();
bindControls();
setStatus("idle", "Idle");
setLatency();
