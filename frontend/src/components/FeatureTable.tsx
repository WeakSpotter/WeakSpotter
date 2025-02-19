// src/components/FeatureTable.tsx
import Icon from "@mdi/react";
import { mdiCheck, mdiClose } from "@mdi/js";

const features = [
  ["Basic Vulnerability Check", true, true],
  ["DNS Records", true, true],
  ["WHOIS Information", true, true],
  ["Cloudflare Detection", true, true],
  ["Nmap Scan", false, true],
  ["HTTP Version Check", false, true],
] as const;

export default function FeatureTable() {
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
        {features.map(([feature, simple, complex], idx) => (
          <tr
            key={idx}
            className={`${idx % 2 === 0 ? "bg-base-200" : "bg-base-300"}`}
          >
            <td className="px-6 py-4">{feature}</td>
            <td className="px-6 py-4">
              <Icon
                path={simple ? mdiCheck : mdiClose}
                size={1}
                className={`m-auto ${simple ? "text-green-500" : "text-red-500"}`}
              />
            </td>
            <td className="px-6 py-4">
              <Icon
                path={complex ? mdiCheck : mdiClose}
                size={1}
                className={`m-auto ${complex ? "text-green-500" : "text-red-500"}`}
              />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
