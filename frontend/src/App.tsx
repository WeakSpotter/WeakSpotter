import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/components/Navbar";
import Footer from "./components/components/Footer";
import ScanList from "./components/pages/ScanList";
import CreateScan from "./components/pages/CreateScan";
import ScanDetails from "./components/pages/ScanDetails";
import Login from "./components/pages/Login";
import Home from "./components/pages/Home";
import Register from "./components/pages/Register";
import ProtectedRoute from "./components/ProtectedRoute";
import About from "./components/pages/About";
import TOSA from "./components/pages/TOSA";
import NotFound from "./components/pages/404";
import History from "./components/pages/History";
import { Toaster } from "react-hot-toast";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-base-200 pb-16">
        <Toaster />
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/create" element={<CreateScan />} />
            <Route path="/scan/:id" element={<ScanDetails />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/scans"
              element={
                <ProtectedRoute>
                  <ScanList />
                </ProtectedRoute>
              }
            />
            <Route path="/about" element={<About />} />
            <Route path="/tos" element={<TOSA />} />
            <Route path="/history" element={<History />} />{" "}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
        {window.__APP_CONFIG__?.ENV === "development" && <Footer />}
      </div>
    </Router>
  );
}

export default App;
