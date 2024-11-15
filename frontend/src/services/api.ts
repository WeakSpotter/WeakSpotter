import axios from "axios";
import { Scan } from "../types/scan";

const API_URL = "http://localhost:8000/api";

export const api = {
  getScans: () => axios.get<Scan[]>(`${API_URL}/scans/`),
  getScan: (id: number) => axios.get<Scan>(`${API_URL}/scans/${id}`),
  getScanData: (id: number) => axios.get(`${API_URL}/scans/${id}/data`),
  getScanScore: (id: number) =>
    axios.get<number>(`${API_URL}/scans/${id}/score`),
  createScan: (url: string, complex: boolean) =>
    axios.post<Scan>(`${API_URL}/scans/`, null, { params: { url, complex } }),
  deleteScan: (id: number) => axios.delete(`${API_URL}/scans/${id}`),
};
