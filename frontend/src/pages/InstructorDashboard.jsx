import { useCallback, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Plus, Users, Percent, Star, Pencil, ListChecks } from "lucide-react";
import { instructorApi } from "../api/resources";
import { useFetch } from "../hooks/useFetch";
import { useToast } from "../context/ToastContext";
import { extractErrorMessage } from "../api/client";
import { EmptyState, ErrorState, CardGridSkeleton } from "../components/States";

const CATEGORIES = ["Data Science", "Web Development", "Cloud & DevOps", "Design"];

export default function InstructorDashboard() {
  const navigate = useNavigate();
  const { push } = useToast();
  const coursesFetch = useFetch(useCallback(() => instructorApi.myCourses(), []));
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", category: CATEGORIES[0], level: "beginner", duration_hours: 5, tags: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleCreate(e) {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const course = await instructorApi.createCourse({
        ...form,
        duration_hours: Number(form.duration_hours),
        tags: form.tags.split(",").map((t) => t.trim()).filter(Boolean),
      });
      push("Course created");
      navigate(`/instructor/courses/${course.id}`);
    } catch (err) {
      push(extractErrorMessage(err), "error");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-5 py-10">
      <div className="flex items-center justify-between mb-1">
        <h1 className="text-2xl font-display font-semibold">Instructor studio</h1>
        <button onClick={() => setShowCreate((s) => !s)} className="btn-primary text-sm">
          <Plus size={16} /> New course
        </button>
      </div>
      <p className="text-mist mb-8">Your courses, enrollment, and how students are doing.</p>

      {showCreate && (
        <form onSubmit={handleCreate} className="card p-5 mb-8 space-y-3">
          <div className="grid sm:grid-cols-2 gap-3">
            <div>
              <label className="label block mb-1.5">Title</label>
              <input required className="input" value={form.title} onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))} />
            </div>
            <div>
              <label className="label block mb-1.5">Category</label>
              <select className="input" value={form.category} onChange={(e) => setForm((f) => ({ ...f, category: e.target.value }))}>
                {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
          </div>
          <div>
            <label className="label block mb-1.5">Description</label>
            <textarea required className="input min-h-[80px]" value={form.description} onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))} />
          </div>
          <div className="grid sm:grid-cols-3 gap-3">
            <div>
              <label className="label block mb-1.5">Level</label>
              <select className="input" value={form.level} onChange={(e) => setForm((f) => ({ ...f, level: e.target.value }))}>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <div>
              <label className="label block mb-1.5">Duration (hours)</label>
              <input type="number" min="0" step="0.5" className="input" value={form.duration_hours} onChange={(e) => setForm((f) => ({ ...f, duration_hours: e.target.value }))} />
            </div>
            <div>
              <label className="label block mb-1.5">Tags (comma-separated)</label>
              <input className="input" value={form.tags} onChange={(e) => setForm((f) => ({ ...f, tags: e.target.value }))} placeholder="python, pandas" />
            </div>
          </div>
          <div className="flex gap-2">
            <button type="submit" disabled={isSubmitting} className="btn-primary text-sm">{isSubmitting ? "Creating…" : "Create course"}</button>
            <button type="button" onClick={() => setShowCreate(false)} className="btn-ghost text-sm">Cancel</button>
          </div>
        </form>
      )}

      {coursesFetch.isLoading ? (
        <CardGridSkeleton count={3} />
      ) : coursesFetch.error ? (
        <ErrorState description={coursesFetch.error} onRetry={coursesFetch.refetch} />
      ) : coursesFetch.data.length === 0 ? (
        <EmptyState title="No courses yet" description="Create your first course to start building out modules and lessons." />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          {coursesFetch.data.map((stat) => (
            <div key={stat.course.id} className="card p-5">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <span className="badge text-[11px] mb-2" style={{ background: `${stat.course.color}22`, color: stat.course.color }}>{stat.course.category}</span>
                  <h3 className="font-display font-semibold">{stat.course.title}</h3>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-3 mb-4">
                <Stat icon={Users} label="Enrolled" value={stat.enrolled_count} />
                <Stat icon={Percent} label="Avg quiz" value={stat.avg_quiz_score != null ? `${stat.avg_quiz_score}%` : "—"} />
                <Stat icon={Star} label="Completion" value={`${stat.completion_rate}%`} />
              </div>
              <div className="flex gap-2">
                <Link to={`/instructor/courses/${stat.course.id}`} className="btn-secondary text-sm flex-1">
                  <Pencil size={14} /> Edit
                </Link>
                <Link to={`/instructor/courses/${stat.course.id}/roster`} className="btn-secondary text-sm flex-1">
                  <ListChecks size={14} /> Roster
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function Stat({ icon: Icon, label, value }) {
  return (
    <div className="bg-white/5 rounded-xl p-2.5">
      <div className="flex items-center gap-1 text-mist mb-1"><Icon size={11} /><span className="text-[10px] uppercase tracking-wide">{label}</span></div>
      <div className="font-mono text-sm font-medium">{value}</div>
    </div>
  );
}
