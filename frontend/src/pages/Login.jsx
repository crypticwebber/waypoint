import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Compass, LogIn } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { extractErrorMessage } from "../api/client";

export default function Login() {
  const { login } = useAuth();
  const { push } = useToast();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await login(email, password);
      push("Welcome back!");
      navigate("/dashboard");
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-5 py-12">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2 justify-center mb-8">
          <span className="flex items-center justify-center w-9 h-9 rounded-full bg-gradient-to-br from-teal to-amber">
            <Compass size={18} className="text-ink" strokeWidth={2.5} />
          </span>
          <span className="font-display font-semibold text-xl">Waypoint</span>
        </div>

        <div className="card p-7">
          <h1 className="font-display font-semibold text-xl mb-1">Welcome back</h1>
          <p className="text-sm text-mist mb-6">Log in to pick up where you left off.</p>

          {error && (
            <div role="alert" className="bg-coral/10 border border-coral/30 text-coral text-sm rounded-xl px-4 py-3 mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="label block mb-1.5">Email</label>
              <input
                id="email" type="email" required autoComplete="email"
                className="input" value={email} onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
              />
            </div>
            <div>
              <label htmlFor="password" className="label block mb-1.5">Password</label>
              <input
                id="password" type="password" required autoComplete="current-password"
                className="input" value={password} onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
              />
            </div>
            <button type="submit" disabled={isSubmitting} className="btn-primary w-full mt-2">
              <LogIn size={16} /> {isSubmitting ? "Logging in…" : "Log in"}
            </button>
          </form>

          <p className="text-sm text-mist text-center mt-6">
            New here? <Link to="/register" className="text-amber hover:underline">Create an account</Link>
          </p>
        </div>

        <div className="text-center mt-5 text-xs text-mist">
          Demo login: <span className="font-mono">alex.demo@waypoint.dev</span> / <span className="font-mono">waypoint123</span>
        </div>
      </div>
    </div>
  );
}
