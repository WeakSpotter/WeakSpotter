import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-base-200">
      <div className="hero min-h-[50vh] bg-base-200">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">Welcome to WeakSpotter</h1>
            <p className="py-6">
              Discover vulnerabilities in your web applications with ease.
            </p>
            <div className="flex justify-center gap-4">
              <Link to="/create" className="btn btn-primary">
                Get Started
              </Link>
              {!isAuthenticated && (
                <Link to="/register" className="btn btn-secondary">
                  Create Account
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
      <div className="container mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-4 text-center">
          Feature Comparison
        </h2>
        <table className="table-auto w-full bg-white shadow-md rounded-lg">
          <thead>
            <tr>
              <th className="px-4 py-2">Feature</th>
              <th className="px-4 py-2">Simple Scan</th>
              <th className="px-4 py-2">Complex Scan</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border px-4 py-2">Basic Vulnerability Check</td>
              <td className="border px-4 py-2">✔️</td>
              <td className="border px-4 py-2">✔️</td>
            </tr>
            <tr>
              <td className="border px-4 py-2">DNS Records</td>
              <td className="border px-4 py-2">✔️</td>
              <td className="border px-4 py-2">✔️</td>
            </tr>
            <tr>
              <td className="border px-4 py-2">WHOIS Information</td>
              <td className="border px-4 py-2">✔️</td>
              <td className="border px-4 py-2">✔️</td>
            </tr>
            <tr>
              <td className="border px-4 py-2">Cloudflare Detection</td>
              <td className="border px-4 py-2">✔️</td>
              <td className="border px-4 py-2">✔️</td>
            </tr>
            <tr>
              <td className="border px-4 py-2">Nmap Scan</td>
              <td className="border px-4 py-2">❌</td>
              <td className="border px-4 py-2">✔️</td>
            </tr>
            <tr>
              <td className="border px-4 py-2">HTTP Version Check</td>
              <td className="border px-4 py-2">❌</td>
              <td className="border px-4 py-2">✔️</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
