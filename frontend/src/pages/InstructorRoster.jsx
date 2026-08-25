import { useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { instructorApi } from "../api/resources";
import { useFetch } from "../hooks/useFetch";
import { RouteProgress } from "../components/RouteLine";
import { EmptyState, ErrorState, LineSkeleton } from "../components/States";

export default function InstructorRoster() {
  const { courseId } = useParams();
  const rosterFetch = useFetch(useCallback(() => instructorApi.roster(courseId), [courseId]), [courseId]);

  return (
    <div className="max-w-4xl mx-auto px-5 py-10">
      <Link to="/instructor" className="flex items-center gap-1.5 text-sm text-mist hover:text-paper mb-6">
        <ArrowLeft size={15} /> Back to studio
      </Link>
      <h1 className="text-2xl font-display font-semibold mb-1">Student roster</h1>
      <p className="text-mist mb-8">Who's enrolled, and how far along they are.</p>

      {rosterFetch.isLoading ? (
        <div className="space-y-3">{Array.from({ length: 4 }).map((_, i) => <LineSkeleton key={i} className="h-16" />)}</div>
      ) : rosterFetch.error ? (
        <ErrorState description={rosterFetch.error} onRetry={rosterFetch.refetch} />
      ) : rosterFetch.data.length === 0 ? (
        <EmptyState title="No students enrolled yet" description="Once someone enrolls, they'll show up here with live progress." />
      ) : (
        <div className="card divide-y divide-white/5">
          {rosterFetch.data.map((s) => (
            <div key={s.user_id} className="p-4 grid grid-cols-[1fr_auto] sm:grid-cols-[1fr_auto_140px] items-center gap-4">
              <div className="min-w-0">
                <p className="font-medium text-sm truncate">{s.full_name}</p>
                <p className="text-xs text-mist truncate">{s.email}</p>
              </div>
              <span className="text-xs text-mist hidden sm:block">Enrolled {new Date(s.enrolled_at).toLocaleDateString()}</span>
              <div className="w-full sm:w-[140px]">
                <RouteProgress percent={s.progress_pct} showPercent />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
