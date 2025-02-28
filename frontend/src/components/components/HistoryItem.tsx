import { Scan } from "../../types/scan";
import { ScoreCircle } from "./ScoreCircle";
import { Line, LineChart, ResponsiveContainer, Tooltip } from "recharts";

interface HistoryItemProps {
  website: string;
  scans: Scan[];
}

export const HistoryItem: React.FC<HistoryItemProps> = ({ website, scans }) => {
  // Sort scans by date
  const sortedScans = [...scans].sort(
    (a, b) =>
      new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
  );

  // Get the latest score
  const latestScore = sortedScans[sortedScans.length - 1]?.score ?? null;

  // Prepare data for the chart
  const chartData = sortedScans
    .filter((scan) => scan.score !== null)
    .map((scan) => ({
      date: new Date(scan.created_at).getTime(),
      score: scan.score,
    }));

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="card-title">{website}</h3>
            <p className="text-sm text-base-content/70">
              {scans.length} scan{scans.length !== 1 ? "s" : ""}
            </p>
          </div>
          {latestScore !== null && (
            <div className="flex items-center">
              <ScoreCircle score={latestScore} size="sm" />
            </div>
          )}
        </div>

        <div className="h-24 mt-4">
          {chartData.length > 1 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="currentColor"
                  strokeWidth={2}
                  dot={false}
                />
                <Tooltip
                  content={({ payload }) => {
                    if (payload && payload.length > 0) {
                      const data = payload[0].payload;
                      return (
                        <div className="bg-base-200 p-2 rounded shadow">
                          <p className="text-sm">Score: {data.score}</p>
                          <p className="text-xs text-base-content/70">
                            {new Date(data.date).toLocaleDateString()}
                          </p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-full text-base-content/50">
              Not enough data for graph
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
