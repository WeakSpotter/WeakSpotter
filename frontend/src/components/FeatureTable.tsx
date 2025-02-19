import { useEffect, useState } from "react";
import Icon from "@mdi/react";
import { mdiCheck, mdiClose, mdiLoading } from "@mdi/js";
import { api } from "../services/api";

export default function FeatureTable() {
  const [features, setFeatures] = useState<{
    simple: string[];
    complex: string[];
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFeatures = async () => {
      try {
        const response = await api.getInfo();
        setFeatures(response.data);
      } catch (err) {
        setError("Failed to load features");
        console.error("Error fetching features:", err);
      }
    };

    fetchFeatures();
  }, []);

  if (error) {
    return (
      <div className="text-center text-error">
        <p>{error}</p>
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
        {allFeatures.map((feature, idx) => (
          <tr
            key={idx}
            className={`${idx % 2 === 0 ? "bg-base-200" : "bg-base-300"}`}
          >
            <td className="px-6 py-4">{feature}</td>
            <td className="px-6 py-4">
              <Icon
                path={features.simple.includes(feature) ? mdiCheck : mdiClose}
                size={1}
                className={`m-auto ${
                  features.simple.includes(feature)
                    ? "text-green-500"
                    : "text-red-500"
                }`}
              />
            </td>
            <td className="px-6 py-4">
              <Icon
                path={features.complex.includes(feature) ? mdiCheck : mdiClose}
                size={1}
                className={`m-auto ${
                  features.complex.includes(feature)
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
