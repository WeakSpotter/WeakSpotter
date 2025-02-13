import { useState, useEffect } from "react";
import { api } from "../services/api";
import toast from "react-hot-toast";

interface ScanResult {
  id: number;
  title: string;
  description: string;
  score: number;
}

interface ScanListResultProps {
  scan: any
}

export default function ScanListResult({ scan }: ScanListResultProps) {
  const [showModal, setShowModal] = useState(false);
  const [selectedResult, setSelectedResult] = useState<ScanResult | null>(null);
  const [scanResults, setScanResults] = useState<Record<number, ScanResult>>({});

  useEffect(() => {
    const fetchScanResults = async () => {
      try {
        const results = await Promise.all(
          scan.result.map(async (id : number) => {
            const res = await api.getScanResult(id);
            return { id, ...res.data };
          })
        );
        
        const resultsMap = results.reduce((acc, result) => {
          acc[result.id] = result;
          return acc;
        }, {} as Record<number, ScanResult>);
        
        setScanResults(resultsMap);
      } catch (error) {
        toast.error("Failed to load scan results. Please try again.");
        console.error("Error loading scan results:", error);
      }
    };

    if (scan?.result?.length > 0) {
      fetchScanResults();
    }
  }, [scan.result]);

  const handleMoreDetails = async (id: number) => {
    if (!id) return;

    try {
      const res = await api.getScanResult(id);
      setSelectedResult(res.data);
      setShowModal(true);
    } catch (error) {
      toast.error("Failed to load scan result. Please try again.");
      console.error("Error loading scan result:", error);
    }
  };

  const handleCloseModal = (event: React.MouseEvent<HTMLDivElement>) => {
    if ((event.target as HTMLElement).classList.contains("modal")) {
      setShowModal(false);
    }
  };

  if (!scan?.result?.length) {
    return <div className="alert alert-error mt-5">Scan results not found</div>;
  }

  return (
    <>
      {scan.result.map((id: number) => {
        const result = scanResults[id];
        if (!result) return null;

        return (
          <div key={id} className="card bg-base-100 shadow-xl mt-5">
            <div className="card-body">
              <div className="flex justify-between items-center">
                <h2 className="card-title">{result.title}</h2>
                <h4>{result.score}</h4>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p>{result.description}</p>
                </div>
              </div>

              <div className="card-actions justify-end">
                <button
                  className="btn btn-primary"
                  onClick={() => handleMoreDetails(id)}
                >
                  More details
                </button>
              </div>
            </div>
          </div>
        );
      })}

      {showModal && selectedResult && (
        <div className="modal modal-open" onClick={handleCloseModal}>
          <div className="modal-box max-w-3xl">
            <h3 className="font-bold text-lg">{selectedResult.title}</h3>
            <pre className="mt-4 overflow-x-auto bg-base-200 p-4 rounded-lg">
              {JSON.stringify(selectedResult, null, 2)}
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