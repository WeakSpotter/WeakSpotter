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

axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

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
    axiosInstance.post<{ token: string }>(
      `${API_URL}/auth/login/`,
      new URLSearchParams(credentials),
    ),
  register: (credentials: { username: string; password: string }) =>
    axiosInstance.post<{ token: string }>(`${API_URL}/users/`, credentials),
};
