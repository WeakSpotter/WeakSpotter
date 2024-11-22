import { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import { api } from "../services/api";
import {
  Scan,
  getScanStatusText,
  getScanStatusClass,
  ScanStatus,
} from "../types/scan";
import { ScoreCircle } from "./ScoreCircle";

export default function ScanDetails() {
  const { id } = useParams<{ id: string }>();
  const [scan, setScan] = useState<Scan | null>(null);
  const [score, setScore] = useState<number | null>(null);
  const [data, setData] = useState<any | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);

  // Function to load scan details
  const loadScanDetails = useCallback(async () => {
    if (!id) return;

    try {
      const [scanRes, scoreRes] = await Promise.all([
        api.getScan(parseInt(id)),
        api.getScanScore(parseInt(id)),
      ]);
      setScan(scanRes.data);
      setScore(scoreRes.data);
    } catch (error) {
      console.error("Error loading scan details:", error);
    } finally {
      setLoading(false);
    }
  }, [id]);

  // Setup polling
  useEffect(() => {
    let intervalId: number;

    const startPolling = () => {
      // Initial load
      loadScanDetails();

      // Setup interval for polling
      intervalId = window.setInterval(() => {
        if (
          scan?.status === ScanStatus.pending ||
          scan?.status === ScanStatus.running
        ) {
          loadScanDetails();
        }
      }, 5000); // Poll every 5 seconds
    };

    startPolling();

    // Cleanup function
    return () => {
      if (intervalId) {
        window.clearInterval(intervalId);
      }
    };
  }, [loadScanDetails, scan?.status]);

  const handleViewData = async () => {
    if (!id) return;

    try {
      const response = await api.getScanData(parseInt(id));
      setData(response.data);
      setShowModal(true);
    } catch (error) {
      console.error("Error loading scan data:", error);
    }
  };

  if (loading)
    return (
      <div className="flex justify-center items-center h-64">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );

  if (!scan) return <div className="alert alert-error">Scan not found</div>;

  const isRefreshing =
    scan.status === ScanStatus.pending || scan.status === ScanStatus.running;

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        <div className="flex justify-between items-center">
          <h2 className="card-title">Scan Details</h2>
          {isRefreshing && (
            <div className="flex items-center gap-2">
              <span className="loading loading-spinner loading-sm"></span>
              <span className="text-sm">Refreshing...</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p>
              <strong>ID:</strong> {scan.id}
            </p>
            <p>
              <strong>URL:</strong> {scan.url}
            </p>
            <p>
              <strong>Status:</strong>
              <span className={`badge ml-2 ${getScanStatusClass(scan.status)}`}>
                {getScanStatusText(scan.status)}
              </span>
            </p>
            <p>
              <strong>Created:</strong>{" "}
              {new Date(scan.created_at).toLocaleString()}
            </p>
          </div>
          <div className="flex flex-col items-center justify-center">
            {score !== null ? (
              <>
                <h3 className="font-semibold mb-2">Security Score</h3>
                <ScoreCircle score={score} size="md" />
              </>
            ) : (
              <div className="text-center">
                <h3 className="font-semibold mb-2">Security Score</h3>
                <span className="text-gray-500">-</span>
              </div>
            )}
          </div>
        </div>

        <div className="card-actions justify-end">
          <button
            onClick={handleViewData}
            className="btn btn-primary"
            disabled={
              scan.status !== ScanStatus.completed &&
              scan.status !== ScanStatus.failed
            }
          >
            View Data
          </button>
        </div>
      </div>

      {showModal && (
        <div className="modal modal-open">
          <div className="modal-box max-w-3xl">
            <h3 className="font-bold text-lg">Scan Data</h3>
            <pre className="mt-4 overflow-x-auto bg-base-200 p-4 rounded-lg">
              {JSON.stringify(data, null, 2)}
            </pre>
            <div className="modal-action">
              <button onClick={() => setShowModal(false)} className="btn">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
