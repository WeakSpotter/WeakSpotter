import {
  getScanStatusClass,
  getScanStatusText,
  getScanTypeText,
  Scan,
  ScanStatus,
} from "../types/scan";
import { ScoreCircle } from "./ScoreCircle";

interface ScanHeroProps {
  scan: Scan;
  score: number | null;
  handleViewData: () => void;
}

export const ScanHero: React.FC<ScanHeroProps> = ({
  scan,
  score,
  handleViewData,
}) => {
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
              <strong>Type:</strong> {getScanTypeText(scan.type)}
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
            <p>
              <strong>Progress:</strong> {scan.progress}%
            </p>
            <p>
              <strong>Current Step:</strong> {scan.current_step}
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
    </div>
  );
};
