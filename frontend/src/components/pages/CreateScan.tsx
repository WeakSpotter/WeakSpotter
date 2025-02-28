import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../services/api";
import { useAuth } from "../../context/AuthContext";
import { toast } from "react-hot-toast";
import { AxiosError } from "axios";

export default function CreateScan() {
  const [url, setUrl] = useState("");
  const [complex, setComplex] = useState(false);
  const [loading, setLoading] = useState(false);
  const [acceptedTOS, setAcceptedTOS] = useState(false);
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const formatUrl = (input: string) => {
    input = input.trim();
    if (!/^https?:\/\//i.test(input)) {
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
      toast.success("Scan created successfully.");
    } catch (error) {
      const axiosError = error as AxiosError;

      switch (axiosError.response?.status) {
        case 400:
          toast.error("Invalid URL. Please enter a valid URL.");
          break;
        case 401:
          toast.error("Please log in to access the complex scan feature.");
          break;
        case 403:
          toast.error("You are not authorized to create a scan.");
          break;
        case 409:
          toast.error(
            "A scan for this URL already exists. Please wait at least 1 hour before scanning again.",
          );
          break;
        default:
          toast.error("Failed to create scan. Please try again.");
          break;
      }

      console.error("Error creating scan:", error);
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
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="example.com"
              className="input input-bordered"
              required
            />
          </div>

          <div className="form-control">
            <label className="label cursor-pointer">
              <span className="label-text">Scan Type</span>
              <div className="flex items-center space-x-2">
                <span className="label-text">Simple</span>
                <input
                  type="checkbox"
                  checked={complex}
                  onChange={(e) => setComplex(e.target.checked)}
                  className="toggle toggle-primary"
                />
                <span className="label-text">Complex</span>
              </div>
            </label>
            {!isAuthenticated && (
              <p className="text-sm text-red-500 mt-2">
                Please log in to run a scan.
              </p>
            )}
          </div>

          <div className="form-control mt-4">
            <label className="label cursor-pointer">
              <input
                type="checkbox"
                checked={acceptedTOS}
                onChange={(e) => setAcceptedTOS(e.target.checked)}
                className="checkbox"
                required
              />
              <span className="label-text ml-2">
                I have read and agree to the{" "}
                <a
                  href="/tos"
                  className="link link-primary"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Terms and Conditions
                </a>
              </span>
            </label>
          </div>

          <div className="card-actions justify-end mt-4">
            <button
              type="submit"
              className={`btn btn-primary ${loading ? "loading" : ""}`}
              disabled={loading || !acceptedTOS}
            >
              Start Scan
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
