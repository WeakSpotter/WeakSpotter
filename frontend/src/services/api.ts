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

export const api = {
  getVersion: () => axios.get<{ version: string }>(`${API_URL}/version/`),
  getScans: () => axios.get<Scan[]>(`${API_URL}/scans/`),
  getScan: (id: number) => axios.get<Scan>(`${API_URL}/scans/${id}`),
  getScanData: (id: number) => axios.get(`${API_URL}/scans/${id}/data`),
  getScanScore: (id: number) =>
    axios.get<number>(`${API_URL}/scans/${id}/score`),
  createScan: (url: string, complex: boolean) =>
    axios.post<Scan>(`${API_URL}/scans/`, null, { params: { url, complex } }),
  deleteScan: (id: number) => axios.delete(`${API_URL}/scans/${id}`),
  login: (credentials: { username: string; password: string }) =>
    axios.post<{ token: string }>(`${API_URL}/auth/login/`, credentials),
};
