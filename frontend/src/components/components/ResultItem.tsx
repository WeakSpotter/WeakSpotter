import { useState } from "react";
import Icon from "@mdi/react";
import { mdiChevronDown, mdiChevronUp } from "@mdi/js";
import {
  getCategoryLabel,
  getSeverityClass,
  getSeverityLabel,
  Result,
} from "../../types/scan";

interface ResultProps {
  result: Result;
}

export const ResultItem: React.FC<ResultProps> = ({ result }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpanded = () => setIsExpanded(!isExpanded);

  return (
    <div className="card bg-base-100 shadow-lg mb-4">
      <div
        className="card-body p-4 cursor-pointer"
        onClick={toggleExpanded}
        role="button"
        tabIndex={0}
      >
        <div className="flex justify-between items-center">
          <div className="flex-1 flex justify-start">
            <div
              className={`w-20 flex items-center justify-center ${result.score > 0 ? "text-success" : result.score < 0 ? "text-error" : ""}`}
              style={{
                fontSize: "1.5rem",
              }}
            >
              {result.score > 0 ? `+${result.score}` : result.score}
            </div>
            <div className="flex-1">
              <h3 className="card-title text-lg">{result.title}</h3>
              <p className="text-sm mt-1">{result.short_description}</p>
              <div className="flex gap-2 mt-2">
                <span className={`badge ${getSeverityClass(result.severity)}`}>
                  {getSeverityLabel(result.severity)}
                </span>
                <span className="badge badge-neutral">
                  {getCategoryLabel(result.category)}
                </span>
              </div>
            </div>
          </div>
          <Icon
            path={isExpanded ? mdiChevronUp : mdiChevronDown}
            size={1}
            className="text-base-content"
          />
        </div>

        {isExpanded && (
          <div className="mt-4 space-y-4">
            {result.description && (
              <div className="bg-base-200 p-4 rounded-lg">
                <h4 className="font-semibold mb-2">Description</h4>
                <p className="whitespace-pre-wrap">{result.description}</p>
              </div>
            )}

            {result.recommendation && (
              <div className="bg-base-200 p-4 rounded-lg">
                <h4 className="font-semibold mb-2">Recommendation</h4>
                <p className="whitespace-pre-wrap">{result.recommendation}</p>
              </div>
            )}

            <div className="text-sm text-base-content/70">
              ID: {result.id} | Scan ID: {result.scan_id}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
