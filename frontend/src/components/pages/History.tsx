import { useEffect, useState } from "react";
import { api } from "../../services/api";
import { Scan } from "../../types/scan";
import { HistoryItem } from "../components/HistoryItem";

export default function History() {
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchScans = async () => {
      try {
        const response = await api.getScans();
        setScans(response.data);
      } catch (err) {
        setError("Failed to load scan history");
        console.error("Error fetching scans:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchScans();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-error">
        <span>{error}</span>
      </div>
    );
  }

  // Group scans by website
  const scansByWebsite = scans.reduce(
    (acc, scan) => {
      const website = scan.url.replace(/^https?:\/\//, "");
      if (!acc[website]) {
        acc[website] = [];
      }
      acc[website].push(scan);
      return acc;
    },
    {} as Record<string, Scan[]>,
  );

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Score History</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Object.entries(scansByWebsite).map(([website, scans]) => (
          <HistoryItem key={website} website={website} scans={scans} />
        ))}
      </div>
    </div>
  );
}
