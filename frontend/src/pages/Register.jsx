import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Compass, ArrowRight } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { extractErrorMessage } from "../api/client";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: "", email: "", password: "", role: "student" });
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    if (form.password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    setIsSubmitting(true);
    try {
      const user = await register(form);
      navigate(user.role === "instructor" ? "/instructor" : "/onboarding");
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
          <h1 className="font-display font-semibold text-xl mb-1">Create your account</h1>
          <p className="text-sm text-mist mb-6">Takes under a minute. The good part comes next.</p>

          {error && (
            <div role="alert" className="bg-coral/10 border border-coral/30 text-coral text-sm rounded-xl px-4 py-3 mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="full_name" className="label block mb-1.5">Full name</label>
              <input id="full_name" required className="input" value={form.full_name}
                onChange={(e) => update("full_name", e.target.value)} placeholder="Jordan Rivera" />
            </div>
            <div>
              <label htmlFor="email" className="label block mb-1.5">Email</label>
              <input id="email" type="email" required autoComplete="email" className="input" value={form.email}
                onChange={(e) => update("email", e.target.value)} placeholder="you@example.com" />
            </div>
            <div>
              <label htmlFor="password" className="label block mb-1.5">Password</label>
              <input id="password" type="password" required autoComplete="new-password" className="input" value={form.password}
                onChange={(e) => update("password", e.target.value)} placeholder="At least 8 characters" />
            </div>
            <div>
              <span className="label block mb-1.5">I'm joining as</span>
              <div className="grid grid-cols-2 gap-2">
                {["student", "instructor"].map((role) => (
                  <button
                    key={role} type="button" onClick={() => update("role", role)}
                    className={`rounded-xl border px-3 py-2.5 text-sm font-medium capitalize transition-colors ${
                      form.role === role ? "border-amber bg-amber/10 text-amber" : "border-white/10 text-mist hover:border-white/25"
                    }`}
                  >
                    {role}
                  </button>
                ))}
              </div>
            </div>
            <button type="submit" disabled={isSubmitting} className="btn-primary w-full mt-2">
              {isSubmitting ? "Creating account…" : "Continue"} <ArrowRight size={16} />
            </button>
          </form>

          <p className="text-sm text-mist text-center mt-6">
            Already have an account? <Link to="/login" className="text-amber hover:underline">Log in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
