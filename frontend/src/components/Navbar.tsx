import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="navbar bg-base-100">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost text-xl">
          WeakSpotter
        </Link>
      </div>
      <div className="flex-none">
        <Link to="/create" className="btn btn-primary">
          New Scan
        </Link>
      </div>
    </div>
  );
}
