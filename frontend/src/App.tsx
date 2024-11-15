import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ScanList from "./components/ScanList";
import CreateScan from "./components/CreateScan";
import ScanDetails from "./components/ScanDetails";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-base-200">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<ScanList />} />
            <Route path="/create" element={<CreateScan />} />
            <Route path="/scan/:id" element={<ScanDetails />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
