const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function buildHeaders(token, hasJsonBody = false) {
  const headers = {};
  if (hasJsonBody) {
    headers["Content-Type"] = "application/json";
  }
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
}

function formatErrorDetail(detail) {
  if (detail == null) return "Request failed";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => (typeof item === "object" && item?.msg ? item.msg : String(item)))
      .join(" ");
  }
  return JSON.stringify(detail);
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  if (!response.ok) {
    let detail = "Request failed";
    try {
      const payload = await response.json();
      detail = formatErrorDetail(payload.detail ?? payload);
    } catch {
      detail = response.statusText || detail;
    }
    throw new Error(`${response.status}: ${detail}`);
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

export async function registerUser(username, password) {
  return request("/auth/register", {
    method: "POST",
    headers: buildHeaders(null, true),
    body: JSON.stringify({ username, password }),
  });
}

export async function login(username, password) {
  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);
  return request("/auth/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form,
  });
}

export async function getCurrentUser(token) {
  return request("/users/me", { headers: buildHeaders(token) });
}

export async function listBooks(token, mineOnly = false) {
  return request(`/books?mine_only=${mineOnly}`, { headers: buildHeaders(token) });
}

export async function createBook(token, payload) {
  return request("/books", {
    method: "POST",
    headers: buildHeaders(token, true),
    body: JSON.stringify(payload),
  });
}

export async function updateBook(token, id, payload) {
  return request(`/books/${id}`, {
    method: "PUT",
    headers: buildHeaders(token, true),
    body: JSON.stringify(payload),
  });
}

export async function deleteBook(token, id) {
  return request(`/books/${id}`, {
    method: "DELETE",
    headers: buildHeaders(token),
  });
}

export async function externalSearch(token, query, provider) {
  const encoded = encodeURIComponent(query);
  return request(`/books/external/search?q=${encoded}&provider=${provider}`, {
    headers: buildHeaders(token),
  });
}
