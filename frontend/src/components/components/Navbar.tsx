import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Navbar() {
  const { isAuthenticated, username, logout } = useAuth();

  return (
    <div className="navbar bg-base-100">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost text-xl">
          <span className="hidden md:inline">WeakSpotter</span>
          <span className="md:hidden">WS</span>
        </Link>
        <Link to="/about" className="ml-4 hidden md:inline">
          About
        </Link>
      </div>
      <div className="flex-none gap-2">
        <ul className="menu menu-horizontal px-1">
          {isAuthenticated && (
            <>
              <li>
                <Link to="/create">New Scan</Link>
              </li>
              <li>
                <Link to="/scans">My Scans</Link>
              </li>
              <li>
                <Link to="/history">History</Link>
              </li>
            </>
          )}
        </ul>
        {isAuthenticated ? (
          <div className="dropdown dropdown-end mr-3">
            <div
              tabIndex={0}
              role="button"
              className="btn btn-ghost btn-circle avatar"
            >
              <div className="w-10 rounded-full bg-neutral text-neutral-content content-center">
                <span className="text-xl content-center">
                  {username.charAt(0).toUpperCase()}
                </span>
              </div>
            </div>
            <ul
              tabIndex={0}
              className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
            >
              <li>
                <button onClick={logout}>Logout</button>
              </li>
            </ul>
          </div>
        ) : (
          <Link to="/login" className="btn btn-primary mr-3">
            Login
          </Link>
        )}
      </div>
    </div>
  );
}
