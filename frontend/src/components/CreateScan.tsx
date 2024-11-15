import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";

export default function CreateScan() {
  const [url, setUrl] = useState("");
  const [complex, setComplex] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const formatUrl = (input: string) => {
    // Remove any leading/trailing whitespace
    input = input.trim();

    // Check if the URL already starts with a protocol
    if (!/^https?:\/\//i.test(input)) {
      // Add https:// if no protocol is present
      return `https://${input}`;
    }
    return input;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formattedUrl = formatUrl(url);
      const response = await api.createScan(formattedUrl, complex);
      navigate(`/scan/${response.data.id}`);
    } catch (error) {
      console.error("Error creating scan:", error);
      alert("Failed to create scan");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card bg-base-100 shadow-xl max-w-xl mx-auto">
      <div className="card-body">
        <h2 className="card-title">Create New Scan</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-control">
            <label className="label">
              <span className="label-text">URL to scan</span>
            </label>
            <input
              type="text" // Changed from type="url" to type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="example.com"
              className="input input-bordered"
              required
            />
          </div>

          <div className="form-control">
            <label className="label cursor-pointer">
              <span className="label-text">Complex Scan</span>
              <input
                type="checkbox"
                checked={complex}
                onChange={(e) => setComplex(e.target.checked)}
                className="checkbox"
              />
            </label>
          </div>

          <div className="card-actions justify-end mt-4">
            <button
              type="submit"
              className={`btn btn-primary ${loading ? "loading" : ""}`}
              disabled={loading}
            >
              Start Scan
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
