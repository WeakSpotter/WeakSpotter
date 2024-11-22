import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ScanList from "./components/ScanList";
import CreateScan from "./components/CreateScan";
import ScanDetails from "./components/ScanDetails";
import Login from "./components/Login";


function App() {
  return (
    <Router>
      <div className="min-h-screen bg-base-200 pb-16">
        {" "}
        {/* Added pb-16 for footer space */}
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<ScanList />} />
            <Route path="/create" element={<CreateScan />} />
            <Route path="/scan/:id" element={<ScanDetails />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
