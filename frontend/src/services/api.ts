import axios from "axios";
import { Result, Scan, Job } from "../types/scan";

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
  getScanResults: (id: number) =>
    axiosInstance.get<Result[]>(`${API_URL}/scans/${id}/results`),
  getScanData: (id: number) => axiosInstance.get(`${API_URL}/scans/${id}/data`),
  getInfo: () =>
    axiosInstance.get<{ simple: Job[]; complex: Job[] }>(`${API_URL}/info/`),
  createScan: (url: string, complex: boolean) =>
    axiosInstance.post<Scan>(`${API_URL}/scans/`, null, {
      params: { url, complex },
    }),
  deleteScan: (id: number) => axiosInstance.delete(`${API_URL}/scans/${id}`),
  getScanReport: (id: number) =>
    axiosInstance.get(`${API_URL}/scans/${id}/report`, {
      responseType: "blob",
    }),
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
