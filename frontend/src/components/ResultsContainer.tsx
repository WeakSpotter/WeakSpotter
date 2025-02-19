import { useState } from "react";
import { ResultItem } from "./ResultItem";
import { getCategoryLabel, Result } from "../types/scan";

interface ResultsContainerProps {
  results: Result[];
}

export const ResultsContainer: React.FC<ResultsContainerProps> = ({
  results,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);

  if (!results || results.length === 0) {
    return (
      <div className="alert alert-info mt-4">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          className="stroke-current shrink-0 w-6 h-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          ></path>
        </svg>
        <span>No results available yet.</span>
      </div>
    );
  }

  const categories = Array.from(
    new Set(results.map((result) => result.category)),
  );

  const filteredResults =
    selectedCategory !== null
      ? results.filter((result) => result.category === selectedCategory)
      : results;

  const sortedResults = [...filteredResults].sort(
    (a, b) => b.severity - a.severity,
  );

  return (
    <div className="mt-4 space-y-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Scan Results</h2>
        <div className="flex gap-2">
          <button
            className={`btn ${selectedCategory === null ? "btn-primary" : "btn-outline"}`}
            onClick={() => setSelectedCategory(null)}
          >
            All
          </button>
          {categories.map((category) => (
            <button
              key={category}
              className={`btn ${selectedCategory === category ? "btn-primary" : "btn-outline"}`}
              onClick={() => setSelectedCategory(category)}
            >
              {getCategoryLabel(category)}
            </button>
          ))}
        </div>
      </div>
      {sortedResults.map((result) => (
        <ResultItem key={result.id} result={result} />
      ))}
    </div>
  );
};
