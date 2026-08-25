import axios from "axios";

export const BASE_URL = "http://localhost:8000";

export const api = axios.create({ baseURL: BASE_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("waypoint_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Normalize FastAPI's error shape ({ detail: "..." } or a validation array)
// into a single readable string every screen can just display.
export function extractErrorMessage(error) {
  const detail = error?.response?.data?.detail;
  if (!detail) return "Something went wrong. Please try again.";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg || JSON.stringify(d)).join("; ");
  }
  return "Something went wrong. Please try again.";
}

export default api;
