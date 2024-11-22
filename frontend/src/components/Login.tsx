import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api"; // Import de votre fichier API

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Utilisation de la méthode API pour l'authentification
      const response = await api.login({ username, password });

      // Enregistre le token dans le localStorage pour une utilisation future
      localStorage.setItem("authToken", response.data.token);

      // Redirige vers une page sécurisée après la connexion
      navigate("/create");
    } catch (error) {
      console.error("Login failed:", error);
      alert("Invalid username or password. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card bg-base-100 shadow-xl max-w-xl mx-auto">
      <div className="card-body">
        <h2 className="card-title">Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-control">
            <label className="label">
              <span className="label-text">Username</span>
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              className="input input-bordered"
              required
            />
          </div>

          <div className="form-control">
            <label className="label">
              <span className="label-text">Password</span>
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              className="input input-bordered"
              required
            />
          </div>

          <div className="card-actions justify-end mt-4">
            <button
              type="submit"
              className={`btn btn-primary ${loading ? "loading" : ""}`}
              disabled={loading}
            >
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
