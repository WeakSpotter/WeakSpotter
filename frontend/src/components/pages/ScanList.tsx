import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../../services/api";
import {
  Scan,
  getScanStatusText,
  getScanStatusClass,
  ScanStatus,
} from "../../types/scan";
import toast from "react-hot-toast";
import { AxiosError } from "axios";
import Icon from "@mdi/react";
import {
  mdiCheckCircle,
  mdiCloseCircle,
  mdiProgressClock,
  mdiClockOutline,
} from "@mdi/js";

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

  const getStatusIcon = (scanStatus: ScanStatus): JSX.Element | null => {
    switch (scanStatus) {
      case ScanStatus.completed:
        return (
          <Icon path={mdiCheckCircle} size={1} className="text-green-500" />
        );
      case ScanStatus.failed:
        return <Icon path={mdiCloseCircle} size={1} className="text-red-500" />;
      case ScanStatus.running:
        return (
          <Icon path={mdiProgressClock} size={1} className="text-yellow-500" />
        );
      case ScanStatus.pending:
        return (
          <Icon path={mdiClockOutline} size={1} className="text-blue-500" />
        );
      default:
        return null;
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
            <th className="hidden sm:table-cell">Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {scans.map((scan) => (
            <tr key={scan.id}>
              <td>
                {scan.url.length > 17
                  ? `${scan.url.replace(/^https?:\/\//, "").slice(0, 16)}...`
                  : scan.url.replace(/^https?:\/\//, "")}
              </td>
              <td>
                <span
                  className={`badge ${getScanStatusClass(scan.status)} hidden sm:inline`}
                >
                  {getScanStatusText(scan.status)}
                </span>
                <span className="sm:hidden">{getStatusIcon(scan.status)}</span>
              </td>
              <td className="hidden sm:table-cell">
                {new Date(scan.created_at).toLocaleString()}
              </td>
              <td>
                <Link
                  to={`/scan/${scan.id}`}
                  className="btn btn-sm btn-info mr-2 w-20 my-1"
                >
                  View
                </Link>
                <button
                  onClick={() => handleDelete(scan.id)}
                  className="btn btn-sm btn-error w-20 my-1"
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
