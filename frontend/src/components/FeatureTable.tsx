import { useEffect, useState } from "react";
import Icon from "@mdi/react";
import { mdiCheck, mdiClose, mdiLoading } from "@mdi/js";
import { api } from "../services/api";
import axios from "axios";
import { Job } from "../types/scan";

export default function FeatureTable() {
  const [features, setFeatures] = useState<{
    simple: Job[];
    complex: Job[];
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFeatures = async () => {
      try {
        const response = await api.getInfo();
        setFeatures(response.data);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.status === 500) {
          setError(
            "The server is misconfigured. Please contact the administrator.",
          );
        } else {
          setError(
            "The backend is misconfigured. Please contact the administrator. If you are the administrator you fucked up the jobs' config.json file.",
          );
        }
        console.error("Error fetching features:", err);
      }
    };

    fetchFeatures();
  }, []);

  if (error) {
    return (
      <div className="alert alert-error shadow-lg">
        <div className="flex">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="stroke-current flex-shrink-0 h-6 w-6 mr-2"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <span>{error}</span>
        </div>
      </div>
    );
  }

  if (!features) {
    return (
      <div className="text-center">
        <Icon
          path={mdiLoading}
          size={2}
          className="animate-spin inline-block"
        />
        <p>Loading features...</p>
      </div>
    );
  }

  // Combine all features into a single array for rendering
  const allFeatures = Array.from(
    new Set([...features.simple, ...features.complex]),
  );

  const simpleFeaturesNames = features.simple.map((feature) => feature.name);
  const complexFeaturesNames = features.complex.map((feature) => feature.name);

  const allFeaturesNames = allFeatures.map((feature) => feature.name);

  return (
    <table className="table w-full bg-base-100 rounded-lg shadow-xl">
      <thead>
        <tr>
          <th className="px-4 py-2">Feature</th>
          <th className="px-4 py-2 text-center">Simple Scan</th>
          <th className="px-4 py-2 text-center">Complex Scan</th>
        </tr>
      </thead>
      <tbody>
        {allFeaturesNames.map((feature, idx) => (
          <tr
            key={idx}
            className={`${idx % 2 === 0 ? "bg-base-200" : "bg-base-300"}`}
          >
            <td className="px-6 py-4">{feature}</td>
            <td className="px-6 py-4">
              <Icon
                path={
                  simpleFeaturesNames.includes(feature) ? mdiCheck : mdiClose
                }
                size={1}
                className={`m-auto ${
                  simpleFeaturesNames.includes(feature)
                    ? "text-green-500"
                    : "text-red-500"
                }`}
              />
            </td>
            <td className="px-6 py-4">
              <Icon
                path={
                  complexFeaturesNames.includes(feature) ? mdiCheck : mdiClose
                }
                size={1}
                className={`m-auto ${
                  complexFeaturesNames.includes(feature)
                    ? "text-green-500"
                    : "text-red-500"
                }`}
              />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
