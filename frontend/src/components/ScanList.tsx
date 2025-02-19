import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import { Scan, getScanStatusText, getScanStatusClass } from "../types/scan";
import toast from "react-hot-toast";
import { AxiosError } from "axios";

export default function ScanList() {
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadScans();
  }, []);

  const loadScans = async () => {
    try {
      const response = await api.getScans();
      setScans(response.data);
    } catch (error) {
      toast.error("Failed to load scans. Please try again.");
      console.error("Error loading scans:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this scan?")) return;

    try {
      await api.deleteScan(id);
      setScans(scans.filter((scan) => scan.id !== id));
    } catch (error) {
      const axiosError = error as AxiosError;

      switch (axiosError.response?.status) {
        case 403:
          toast.error("You are not authorized to delete this scan.");
          break;
        default:
          toast.error("Failed to delete scan. Please try again.");
          break;
      }

      console.error("Error deleting scan:", error);
    }
  };

  if (loading)
    return (
      <div className="flex justify-center items-center h-64">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );

  return (
    <div className="overflow-x-auto">
      <table className="table bg-base-100">
        <thead>
          <tr>
            <th>URL</th>
            <th>Status</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {scans.map((scan) => (
            <tr key={scan.id}>
              <td>{scan.url}</td>
              <td>
                <span className={`badge ${getScanStatusClass(scan.status)}`}>
                  {getScanStatusText(scan.status)}
                </span>
              </td>
              <td>{new Date(scan.created_at).toLocaleString()}</td>
              <td>
                <Link
                  to={`/scan/${scan.id}`}
                  className="btn btn-sm btn-info mr-2"
                >
                  View
                </Link>
                <button
                  onClick={() => handleDelete(scan.id)}
                  className="btn btn-sm btn-error"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
