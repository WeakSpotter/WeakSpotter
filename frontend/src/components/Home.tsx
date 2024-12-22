import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Icon from "@mdi/react";
import { mdiArrowRight, mdiPlayCircle, mdiCheck, mdiClose } from "@mdi/js";

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-base-200">
      <div className="hero min-h-[50vh] bg-base-200">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">Welcome to WeakSpotter</h1>
            <p className="py-6">
              Discover and address vulnerabilities in your web applications with
              ease and confidence.
            </p>
            <div className="flex justify-center gap-4">
              <Link
                to={isAuthenticated ? "/create" : "/register"}
                className="btn btn-primary flex items-center"
              >
                Get Started
                <Icon path={mdiArrowRight} size={1} className="ml-2" />
              </Link>
              <a
                href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-outline btn-primary flex items-center"
              >
                <Icon path={mdiPlayCircle} size={1} className="mr-2" />
                Watch Demo
              </a>
            </div>
          </div>
        </div>
      </div>
      <div className="container mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-4 text-center">
          Feature Comparison
        </h2>
        <table className="table w-full bg-base-100 rounded-lg shadow-xl">
          <thead>
            <tr>
              <th className="px-4 py-2">Feature</th>
              <th className="px-4 py-2 text-center">Simple Scan</th>
              <th className="px-4 py-2 text-center">Complex Scan</th>
            </tr>
          </thead>
          <tbody>
            {[
              ["Basic Vulnerability Check", true, true],
              ["DNS Records", true, true],
              ["WHOIS Information", true, true],
              ["Cloudflare Detection", true, true],
              ["Nmap Scan", false, true],
              ["HTTP Version Check", false, true],
            ].map(([feature, simple, complex], idx) => (
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
      </div>
    </div>
  );
}
