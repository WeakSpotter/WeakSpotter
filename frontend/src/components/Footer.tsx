import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Footer() {
  const [backendVersion, setBackendVersion] = useState<string>("");
  const frontendVersion = window.__APP_CONFIG__?.COMMIT_HASH || "unknown";

  useEffect(() => {
    const fetchBackendVersion = async () => {
      try {
        const response = await api.getVersion();
        setBackendVersion(response.data.version);
      } catch (error) {
        console.error("Error fetching backend version:", error);
        setBackendVersion("error");
      }
    };

    fetchBackendVersion();
  }, []);

  const frontendBadge = (
    <div className="badge badge-outline">
      Frontend:{" "}
      {frontendVersion.length > 7 ? frontendVersion.slice(-7) : frontendVersion}
    </div>
  );

  const backendBadge = (
    <div className="badge badge-outline">
      Backend:{" "}
      {backendVersion.length > 7 ? backendVersion.slice(-7) : backendVersion}
    </div>
  );

  return (
    <footer className="footer footer-center p-4 bg-base-300 text-base-content fixed bottom-0 w-full">
      {window.__APP_CONFIG__?.ENV === "development" && (
        <div className="flex gap-4">
          {frontendBadge}
          {backendBadge}
        </div>
      )}
    </footer>
  );
}
