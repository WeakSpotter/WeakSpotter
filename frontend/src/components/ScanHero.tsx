import { getScanTypeText, Scan, ScanStatus, ScanType } from "../types/scan";
import { ScoreCircle } from "./ScoreCircle";

interface ScanHeroProps {
  scan: Scan;
  handleViewData: () => void;
}

export const ScanHero: React.FC<ScanHeroProps> = ({ scan, handleViewData }) => {
  const isRefreshing =
    scan.status === ScanStatus.pending || scan.status === ScanStatus.running;

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        <div className="flex justify-between items-center">
          <h2 className="card-title">
            Results for {scan.url}{" "}
            <span
              className={`badge badge-neutral ml-2 ${scan.type === ScanType.simple ? "badge-outline" : ""}`}
            >
              {getScanTypeText(scan.type)}
            </span>
          </h2>
          {isRefreshing && (
            <div className="flex items-center gap-2">
              <span className="loading loading-spinner loading-sm"></span>
              <span className="text-sm">Scanning ({scan.status})...</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p>
              <strong>Created:</strong>{" "}
              {new Date(scan.created_at).toLocaleString()}
            </p>
          </div>
          <div className="flex flex-col items-center justify-center">
            {scan.score !== null ? (
              <>
                <h3 className="font-semibold mb-2">Security Score</h3>
                <ScoreCircle score={scan.score} size="md" />
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
    </div>
  );
};
