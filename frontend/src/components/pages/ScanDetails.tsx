import { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import { api } from "../../services/api";
import { Scan, ScanStatus } from "../../types/scan";
import toast from "react-hot-toast";
import { ScanHero } from "../components/ScanHero";
import { ResultsContainer } from "../components/ResultsContainer";
import { Result } from "../../types/scan";

export default function ScanDetails() {
  const { id } = useParams<{ id: string }>();
  const [scan, setScan] = useState<Scan | null>(null);
  const [results, setResults] = useState<Result[]>([]);
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
    let startTime: number;

    const startPolling = () => {
      loadScanDetails();
      startTime = Date.now();
      intervalId = window.setInterval(() => {
        const elapsedTime = Date.now() - startTime;

        if (
          scan?.status === ScanStatus.pending ||
          scan?.status === ScanStatus.running
        ) {
          loadScanDetails();
        }

        if (elapsedTime >= 30000) {
          window.clearInterval(intervalId);
          intervalId = window.setInterval(loadScanDetails, 5000);
        } else if (elapsedTime >= 5000) {
          window.clearInterval(intervalId);
          intervalId = window.setInterval(loadScanDetails, 1000);
        }
      }, 200);
    };

    startPolling();

    return () => {
      if (intervalId) {
        window.clearInterval(intervalId);
      }
    };
  }, [loadScanDetails, scan?.status]);

  if (loading)
    return (
      <div className="flex justify-center items-center h-64">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );

  if (!scan) return <div className="alert alert-error">Scan not found</div>;

  return (
    <>
      <ScanHero scan={scan} />
      <ResultsContainer results={results} />
    </>
  );
}
