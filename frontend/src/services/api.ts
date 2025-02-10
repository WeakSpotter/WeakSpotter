import axios from "axios";
import { Scan } from "../types/scan";

declare global {
  interface Window {
    __APP_CONFIG__: {
      API_URL: string;
      COMMIT_HASH: string;
      ENV: string;
    };
  }
}

const API_URL = window.__APP_CONFIG__?.API_URL || "http://localhost:8000/api";

const axiosInstance = axios.create({
  baseURL: API_URL,
});

// Add this function to handle logout
const handleLogout = () => {
  localStorage.removeItem("authToken");
  localStorage.removeItem("username");
  // Force reload the page to reset the application state
  window.location.href = "/login";
};

// Request interceptor (unchanged)
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Check if the error is due to an invalid token or authentication
      if (
        error.response.status === 401 &&
        (error.response.data?.detail === "Invalid token" ||
          error.response.data?.detail === "Not authenticated")
      ) {
        handleLogout();
      }
    }
    return Promise.reject(error);
  },
);
export const api = {
  getVersion: () =>
    axiosInstance.get<{ version: string }>(`${API_URL}/version/`),
  getScans: () => axiosInstance.get<Scan[]>(`${API_URL}/scans/`),
  getScan: (id: number) => axiosInstance.get<Scan>(`${API_URL}/scans/${id}`),
  getScanData: (id: number) => axiosInstance.get(`${API_URL}/scans/${id}/data`),
  getScanScore: (id: number) =>
    axiosInstance.get<number>(`${API_URL}/scans/${id}/score`),
  createScan: (url: string, complex: boolean) =>
    axiosInstance.post<Scan>(`${API_URL}/scans/`, null, {
      params: { url, complex },
    }),
  deleteScan: (id: number) => axiosInstance.delete(`${API_URL}/scans/${id}`),
  login: (credentials: { username: string; password: string }) =>
    axiosInstance.post<{ access_token: string }>(
      `${API_URL}/auth/login/`,
      new URLSearchParams(credentials),
    ),
  register: (credentials: { username: string; password: string }) =>
    axiosInstance.post<{ access_token: string }>(
      `${API_URL}/users/`,
      credentials,
    ),
};
