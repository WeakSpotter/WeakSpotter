import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="min-h-[50vh] bg-base-200 flex flex-col items-center justify-center">
      <div className="text-center">
        <h1 className="text-6xl font-bold mb-4">404</h1>
        <h2 className="text-3xl font-semibold mb-4">Page Not Found</h2>
        <p className="text-lg mb-8">
          Sorry, the page you are looking for does not exist.
        </p>
        <Link to="/" className="btn btn-primary">
          Go to Homepage
        </Link>
      </div>
    </div>
  );
}
