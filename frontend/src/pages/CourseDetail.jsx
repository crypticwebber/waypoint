import { useCallback, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { Clock, Users, Star, Circle, PlayCircle, FileQuestion, ChevronDown, ChevronUp } from "lucide-react";
import { coursesApi, learningApi, reviewsApi } from "../api/resources";
import { useFetch } from "../hooks/useFetch";
import { useToast } from "../context/ToastContext";
import { extractErrorMessage } from "../api/client";
import { RouteProgress } from "../components/RouteLine";
import { ErrorState, LineSkeleton } from "../components/States";

const LEVEL_LABEL = { beginner: "Beginner", intermediate: "Intermediate", advanced: "Advanced" };

export default function CourseDetail() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { push } = useToast();
  const [isEnrolling, setIsEnrolling] = useState(false);
  const [openModule, setOpenModule] = useState(0);

  const courseFetch = useFetch(useCallback(() => coursesApi.get(courseId), [courseId]), [courseId]);
  const reviewsFetch = useFetch(useCallback(() => reviewsApi.list(courseId), [courseId]), [courseId]);

  async function handleEnroll() {
    setIsEnrolling(true);
    try {
      await learningApi.enroll(courseId);
      push("Enrolled! Let's get started.");
      await courseFetch.refetch();
    } catch (err) {
      push(extractErrorMessage(err), "error");
    } finally {
      setIsEnrolling(false);
    }
  }

  function goToFirstIncompleteLesson() {
    const course = courseFetch.data;
    // Mirrors the backend's next_incomplete_lesson logic: walk modules/lessons
    // in order and stop at the first lesson not yet completed. completed_lessons
    // is a count (not specific ids), which is safe here because the lesson
    // reader always completes lessons in order and auto-advances forward.
    for (const mod of course.modules) {
      if (mod.completed_lessons < mod.lessons.length) {
        navigate(`/courses/${course.id}/learn/${mod.lessons[mod.completed_lessons].id}`);
        return;
      }
    }
    // Everything complete -- land on the last lesson of the last module.
    const lastModule = course.modules[course.modules.length - 1];
    if (lastModule?.lessons.length) {
      navigate(`/courses/${course.id}/learn/${lastModule.lessons[lastModule.lessons.length - 1].id}`);
    }
  }

  if (courseFetch.isLoading) {
    return (
      <div className="max-w-5xl mx-auto px-5 py-10">
        <LineSkeleton className="w-40 mb-4" />
        <LineSkeleton className="w-2/3 h-8 mb-3" />
        <LineSkeleton className="w-full mb-2" />
        <LineSkeleton className="w-4/5" />
      </div>
    );
  }
  if (courseFetch.error) {
    return <div className="max-w-5xl mx-auto px-5 py-10"><ErrorState description={courseFetch.error} onRetry={courseFetch.refetch} /></div>;
  }

  const course = courseFetch.data;

  return (
    <div className="max-w-5xl mx-auto px-5 py-10">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-6 mb-10">
        <div className="max-w-2xl">
          <div className="flex items-center gap-2 mb-4">
            <span className="badge text-[11px]" style={{ background: `${course.color}22`, color: course.color }}>{course.category}</span>
            <span className="badge bg-white/5 text-mist text-[11px]">{LEVEL_LABEL[course.level]}</span>
          </div>
          <h1 className="text-3xl font-display font-semibold mb-3 leading-tight">{course.title}</h1>
          <p className="text-mist leading-relaxed mb-4">{course.description}</p>
          <div className="flex items-center gap-5 text-sm text-mist flex-wrap">
            <span className="flex items-center gap-1.5"><Clock size={15} /> {course.duration_hours}h</span>
            <span className="flex items-center gap-1.5"><Users size={15} /> {course.enrolled_count} enrolled</span>
            <span className="flex items-center gap-1.5">
              <Star size={15} className={course.avg_rating ? "text-amber fill-amber" : ""} />
              {course.avg_rating ? `${course.avg_rating} (${course.review_count})` : "No reviews yet"}
            </span>
            {course.instructor_name && <span>by {course.instructor_name}</span>}
          </div>
        </div>

        <div className="card p-5 w-full md:w-64 shrink-0">
          {course.is_enrolled && (
            <div className="mb-4">
              <RouteProgress percent={course.progress_pct} label="Your progress" />
            </div>
          )}
          {course.is_enrolled ? (
            <button onClick={goToFirstIncompleteLesson} className="btn-primary w-full">
              <PlayCircle size={16} /> {course.progress_pct > 0 ? "Continue" : "Start course"}
            </button>
          ) : (
            <button onClick={handleEnroll} disabled={isEnrolling} className="btn-primary w-full">
              {isEnrolling ? "Enrolling…" : "Enroll now"}
            </button>
          )}
        </div>
      </div>

      {/* Syllabus */}
      <section className="mb-12">
        <h2 className="text-xl font-display font-semibold mb-4">Syllabus</h2>
        <div className="space-y-2.5">
          {course.modules.map((mod, i) => {
            const isOpen = openModule === i;
            return (
              <div key={mod.id} className="card overflow-hidden">
                <button
                  onClick={() => setOpenModule(isOpen ? -1 : i)}
                  className="w-full flex items-center justify-between px-5 py-4 text-left"
                  aria-expanded={isOpen}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <span className="font-mono text-xs text-mist shrink-0">{String(i + 1).padStart(2, "0")}</span>
                    <div className="min-w-0">
                      <h3 className="font-medium text-sm truncate">{mod.title}</h3>
                      <p className="text-xs text-mist mt-0.5">
                        {mod.lessons.length} lessons{mod.quiz ? " · 1 quiz" : ""}
                        {course.is_enrolled ? ` · ${mod.completed_lessons}/${mod.lessons.length} done` : ""}
                      </p>
                    </div>
                  </div>
                  {isOpen ? <ChevronUp size={16} className="text-mist shrink-0" /> : <ChevronDown size={16} className="text-mist shrink-0" />}
                </button>
                {isOpen && (
                  <div className="px-5 pb-4 border-t border-white/5 pt-2">
                    <ul className="space-y-1">
                      {mod.lessons.map((lesson) => (
                        <li key={lesson.id}>
                          <Link
                            to={course.is_enrolled ? `/courses/${course.id}/learn/${lesson.id}` : "#"}
                            onClick={(e) => !course.is_enrolled && e.preventDefault()}
                            className={`flex items-center gap-2.5 py-2 px-2 -mx-2 rounded-lg text-sm ${course.is_enrolled ? "hover:bg-white/5 text-paper/85" : "text-mist cursor-default"}`}
                          >
                            <Circle size={13} className="text-mist shrink-0" />
                            <span className="flex-1">{lesson.title}</span>
                            <span className="text-xs text-mist shrink-0">{lesson.estimated_minutes}m</span>
                          </Link>
                        </li>
                      ))}
                      {mod.quiz && (
                        <li className="flex items-center gap-2.5 py-2 px-2 -mx-2 text-sm text-mist">
                          <FileQuestion size={13} className="shrink-0" />
                          <span>{mod.quiz.title}</span>
                          <span className="text-xs ml-auto">{mod.quiz.questions.length} questions</span>
                        </li>
                      )}
                    </ul>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* Project */}
      {course.project_brief && (
        <section className="mb-12">
          <h2 className="text-xl font-display font-semibold mb-4">Hands-on project</h2>
          <div className="card p-5">
            <p className="text-sm text-paper/85 leading-relaxed">{course.project_brief}</p>
          </div>
        </section>
      )}

      {/* Reviews */}
      <section>
        <h2 className="text-xl font-display font-semibold mb-4">Reviews</h2>
        {reviewsFetch.isLoading ? (
          <LineSkeleton className="w-full h-20" />
        ) : reviewsFetch.data.length === 0 ? (
          <p className="text-sm text-mist">No reviews yet -- be the first once you've made some progress.</p>
        ) : (
          <div className="space-y-3">
            {reviewsFetch.data.map((r) => (
              <div key={r.id} className="card p-4">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-sm font-medium">{r.user_name}</span>
                  <span className="flex items-center gap-0.5">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <Star key={i} size={13} className={i < r.rating ? "text-amber fill-amber" : "text-white/15"} />
                    ))}
                  </span>
                </div>
                {r.comment && <p className="text-sm text-mist leading-relaxed">{r.comment}</p>}
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
