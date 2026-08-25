import { useCallback } from "react";
import { Link } from "react-router-dom";
import { PlayCircle, Sparkles, Trophy, BookOpen, Target, Percent } from "lucide-react";
import { dashboardApi, recommendationsApi } from "../api/resources";
import { useFetch } from "../hooks/useFetch";
import { useAuth } from "../context/AuthContext";
import { CourseCard } from "../components/CourseCard";
import { RouteProgress } from "../components/RouteLine";
import { CardGridSkeleton, EmptyState, ErrorState, LineSkeleton } from "../components/States";

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="card p-4">
      <div className="flex items-center gap-2 mb-2">
        <Icon size={15} style={{ color }} />
        <span className="label">{label}</span>
      </div>
      <div className="text-2xl font-display font-semibold">{value}</div>
    </div>
  );
}

export default function Dashboard() {
  const { user } = useAuth();
  const stats = useFetch(useCallback(() => dashboardApi.stats(), []));
  const continueLearning = useFetch(useCallback(() => dashboardApi.continueLearning(), []));
  const recommendations = useFetch(useCallback(() => recommendationsApi.mine(6), []));
  const completed = useFetch(useCallback(() => dashboardApi.completed(), []));

  return (
    <div className="max-w-7xl mx-auto px-5 py-10">
      <h1 className="text-2xl font-display font-semibold mb-1">Welcome back, {user?.full_name?.split(" ")[0]}</h1>
      <p className="text-mist mb-8">Here's where your route stands.</p>

      {/* Stats */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
        {stats.isLoading ? (
          Array.from({ length: 4 }).map((_, i) => <div key={i} className="card p-4"><LineSkeleton className="w-20 mb-3" /><LineSkeleton className="w-12 h-7" /></div>)
        ) : stats.error ? (
          <div className="col-span-4"><ErrorState description={stats.error} onRetry={stats.refetch} /></div>
        ) : (
          <>
            <StatCard icon={BookOpen} label="Enrolled" value={stats.data.courses_enrolled} color="#E8A33D" />
            <StatCard icon={Trophy} label="Completed" value={stats.data.courses_completed} color="#2E7D6B" />
            <StatCard icon={Target} label="Lessons done" value={stats.data.lessons_completed} color="#B4507A" />
            <StatCard icon={Percent} label="Avg quiz score" value={stats.data.avg_quiz_score != null ? `${stats.data.avg_quiz_score}%` : "—"} color="#5B4B8A" />
          </>
        )}
      </section>

      {/* Continue learning */}
      <section className="mb-12">
        <div className="flex items-center gap-2 mb-4">
          <PlayCircle size={18} className="text-amber" />
          <h2 className="text-lg font-display font-semibold">Continue learning</h2>
        </div>
        {continueLearning.isLoading ? (
          <CardGridSkeleton count={2} />
        ) : continueLearning.error ? (
          <ErrorState description={continueLearning.error} onRetry={continueLearning.refetch} />
        ) : continueLearning.data.length === 0 ? (
          <EmptyState
            icon={PlayCircle}
            title="Nothing in progress yet"
            description="Enroll in a course from the catalog to see it show up here."
            action={<Link to="/catalog" className="btn-primary">Browse catalog</Link>}
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {continueLearning.data.map((item) => (
              <Link key={item.course.id} to={`/courses/${item.course.id}`} className="card p-5 hover:border-white/15 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <span className="badge text-[11px] mb-2" style={{ background: `${item.course.color}22`, color: item.course.color }}>{item.course.category}</span>
                    <h3 className="font-display font-semibold">{item.course.title}</h3>
                  </div>
                </div>
                <RouteProgress percent={item.progress_pct} />
                {item.next_lesson && (
                  <p className="text-xs text-mist mt-3">Next: <span className="text-paper/80">{item.next_lesson.title}</span></p>
                )}
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* Recommended for you */}
      <section className="mb-12">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles size={18} className="text-teal-bright" />
          <h2 className="text-lg font-display font-semibold">Recommended for you</h2>
        </div>
        {recommendations.isLoading ? (
          <CardGridSkeleton count={3} />
        ) : recommendations.error ? (
          <ErrorState description={recommendations.error} onRetry={recommendations.refetch} />
        ) : recommendations.data.length === 0 ? (
          <EmptyState title="No recommendations yet" description="Complete your preferences to get matched to courses." />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {recommendations.data.map((r) => (
              <CourseCard key={r.course.id} course={r.course} reason={r.reason} />
            ))}
          </div>
        )}
      </section>

      {/* Completed */}
      {!completed.isLoading && !completed.error && completed.data.length > 0 && (
        <section>
          <div className="flex items-center gap-2 mb-4">
            <Trophy size={18} className="text-amber" />
            <h2 className="text-lg font-display font-semibold">Completed</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {completed.data.map((c) => <CourseCard key={c.id} course={c} />)}
          </div>
        </section>
      )}
    </div>
  );
}
