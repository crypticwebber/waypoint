import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function RequireAuth({ children }) {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div className="min-h-[60vh] flex items-center justify-center text-mist text-sm">Loading…</div>;
  }
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
}

export function RequireInstructor({ children }) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <div className="min-h-[60vh] flex items-center justify-center text-mist text-sm">Loading…</div>;
  }
  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== "instructor") return <Navigate to="/dashboard" replace />;
  return children;
}
