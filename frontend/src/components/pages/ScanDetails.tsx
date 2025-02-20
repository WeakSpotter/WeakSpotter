import { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import { api } from "../../services/api";
import { Scan, ScanStatus } from "../../types/scan";
import toast from "react-hot-toast";
import { ScanHero } from "../components/ScanHero";
import { ResultsContainer } from "./ResultsContainer";
import { Result } from "../../types/scan";

export default function ScanDetails() {
  const { id } = useParams<{ id: string }>();
  const [scan, setScan] = useState<Scan | null>(null);
  const [results, setResults] = useState<Result[]>([]);
  const [data, setData] = useState<any | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);

  const loadScanDetails = useCallback(async () => {
    if (!id) return;

    try {
      const [scanRes, resultsRes] = await Promise.all([
        api.getScan(parseInt(id)),
        api.getScanResults(parseInt(id)),
      ]);
      setScan(scanRes.data);
      setResults(resultsRes.data);
    } catch (error) {
      toast.error("Failed to load scan details. Please try again.");
      console.error("Error loading scan details:", error);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    let intervalId: number;

    const startPolling = () => {
      loadScanDetails();
      intervalId = window.setInterval(() => {
        if (
          scan?.status === ScanStatus.pending ||
          scan?.status === ScanStatus.running
        ) {
          loadScanDetails();
        }
      }, 5000);
    };

    startPolling();

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
      toast.error("Failed to load scan data.");
    }
  };

  const handleCloseModal = (event: React.MouseEvent) => {
    if ((event.target as HTMLElement).classList.contains("modal")) {
      setShowModal(false);
    }
  };

  if (loading)
    return (
      <div className="flex justify-center items-center h-64">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );

  if (!scan) return <div className="alert alert-error">Scan not found</div>;

  return (
    <>
      <ScanHero scan={scan} handleViewData={handleViewData} />
      <ResultsContainer results={results} />
      {showModal && (
        <div className="modal modal-open" onClick={handleCloseModal}>
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
    </>
  );
}
