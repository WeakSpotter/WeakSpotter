import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import Icon from "@mdi/react";
import {
  mdiArrowRight,
  mdiPlayCircle,
  mdiShieldCheck,
  mdiMagnify,
  mdiChartLine,
} from "@mdi/js";
import FeatureTable from "../components/FeatureTable";
import scanExample from "../../assets/scan_example.png";
import scanExampleMobile from "../../assets/scan_example_mobile.png";

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-base-200">
      <div className="hero min-h-[50vh] bg-base-200">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">Welcome to WeakSpotter</h1>
            <p className="py-6">
              Discover and address vulnerabilities in your web applications with
              ease and confidence.
            </p>
            <div className="flex justify-center gap-4">
              <Link
                to={isAuthenticated ? "/create" : "/register"}
                className="btn btn-primary flex items-center"
              >
                Get Started
                <Icon path={mdiArrowRight} size={1} className="ml-2" />
              </Link>
              <a
                href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-outline btn-primary flex items-center"
              >
                <Icon path={mdiPlayCircle} size={1} className="mr-2" />
                Watch Demo
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 pt-8 pb-16">
        <div className="flex flex-col lg:flex-row justify-around items-center">
          <div className="flex flex-col items-center text-center p-4">
            <Icon path={mdiShieldCheck} size={2} className="mb-2" />
            <h3 className="text-xl font-bold">Secure</h3>
            <p className="mt-2">
              Ensure your web applications are secure with our comprehensive
              vulnerability scanning.
            </p>
          </div>
          <div className="divider lg:divider-horizontal"></div>
          <div className="flex flex-col items-center text-center p-4">
            <Icon path={mdiMagnify} size={2} className="mb-2" />
            <h3 className="text-xl font-bold">Discover</h3>
            <p className="mt-2">
              Identify potential weaknesses and vulnerabilities in your web
              applications effortlessly.
            </p>
          </div>
          <div className="divider lg:divider-horizontal"></div>
          <div className="flex flex-col items-center text-center p-4">
            <Icon path={mdiChartLine} size={2} className="mb-2" />
            <h3 className="text-xl font-bold">Analyze</h3>
            <p className="mt-2">
              Gain insights and detailed reports to help you understand and fix
              vulnerabilities.
            </p>
          </div>
        </div>
      </div>

      <div>
        <div className="mockup-browser bg-base-300 border shadow-lg max-w-[70vw] mx-auto">
          <div className="mockup-browser-toolbar">
            <div className="input">https://weakspotter.ozeliurs.com</div>
          </div>
          <img
            src={scanExample}
            alt="Scan Example"
            className="max-w-full h-auto hidden md:block"
          />
          <img
            className="max-w-full h-auto block md:hidden"
            src={scanExampleMobile}
            alt="Scan Example"
          />
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-4 text-center">
          Feature Comparison
        </h2>
        <FeatureTable />
      </div>
    </div>
  );
}
