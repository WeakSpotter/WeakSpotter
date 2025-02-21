import { getScanTypeText, Scan, ScanStatus, ScanType } from "../../types/scan";
import { ScoreCircle } from "./ScoreCircle";
import { useEffect, useRef, useState } from "react";

interface ScanHeroProps {
  scan: Scan;
}

export const ScanHero: React.FC<ScanHeroProps> = ({ scan }) => {
  const isRefreshing =
    scan.status === ScanStatus.pending || scan.status === ScanStatus.running;

  const [animatedProgress, setAnimatedProgress] = useState(0);
  const previousProgress = useRef(0);

  useEffect(() => {
    const startTime = Date.now();
    const duration = 500; // Animation duration in milliseconds
    const startProgress = previousProgress.current;
    const endProgress = scan.progress;

    const animate = () => {
      const currentTime = Date.now();
      const elapsed = currentTime - startTime;

      // Easing function (ease-out)
      const easeProgress = (t: number) => 1 - Math.pow(1 - t, 3);

      if (elapsed < duration) {
        const progress = elapsed / duration;
        const easedProgress = easeProgress(progress);
        const currentProgress =
          startProgress + (endProgress - startProgress) * easedProgress;

        setAnimatedProgress(currentProgress);
        requestAnimationFrame(animate);
      } else {
        setAnimatedProgress(endProgress);
        previousProgress.current = endProgress;
      }
    };

    requestAnimationFrame(animate);
  }, [scan.progress]);

  const gradientStyle =
    animatedProgress === 100
      ? { background: "oklch(var(--b1))" }
      : {
          background: `linear-gradient(90deg,
            oklch(var(--su)/.2) ${Math.max(0, animatedProgress)}%,
            oklch(var(--b1)) ${Math.min(100, animatedProgress)}%)`,
        };

  const formattedUrl = scan.url.replace(/^https?:\/\//, "");

  return (
    <div className="card shadow-xl" style={gradientStyle}>
      <div className="card-body">
        <div className="flex items-start md:items-center flex-col md:flex-row justify-between">
          <div className="flex items-start md:items-center flex-col md:flex-row justify-between">
            <h2 className="card-title">
              <span className="hidden sm:block">Results for </span>
              {formattedUrl}{" "}
            </h2>
            <span
              className={`badge badge-neutral ml-0 mt-2 md:ml-2 md:mt-0 ${scan.type === ScanType.simple ? "badge-outline" : ""}`}
            >
              {getScanTypeText(scan.type)}
            </span>
          </div>
          {isRefreshing && (
            <div className="flex items-center gap-2 mt-2 md:mt-0">
              <span className="loading loading-spinner loading-sm"></span>
              <span className="text-sm">Scanning ({scan.current_step})...</span>
            </div>
          )}
        </div>

        <hr className="block sm:hidden my-4" />

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
                <div className="p-4">
                  <ScoreCircle score={scan.score} size="md" />
                </div>
              </>
            ) : (
              <div className="text-center">
                <h3 className="font-semibold mb-2">Security Score</h3>
                <span className="text-gray-500">-</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
