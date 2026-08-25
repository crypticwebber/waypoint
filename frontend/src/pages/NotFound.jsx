import { Link } from "react-router-dom";
import { Compass, ArrowLeft } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-5 text-center">
      <div>
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-white/5 mb-5">
          <Compass size={28} className="text-mist" />
        </div>
        <h1 className="text-2xl font-display font-semibold mb-2">Off the route</h1>
        <p className="text-mist mb-6 max-w-sm">This page doesn't exist, or you don't have access to it.</p>
        <Link to="/" className="btn-primary"><ArrowLeft size={16} /> Back to Waypoint</Link>
      </div>
    </div>
  );
}
