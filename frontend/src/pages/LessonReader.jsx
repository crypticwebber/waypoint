import { useCallback, useMemo, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import confetti from "canvas-confetti";
import { ChevronLeft, ChevronRight, CheckCircle2, Clock } from "lucide-react";
import { coursesApi, learningApi } from "../api/resources";
import { useFetch } from "../hooks/useFetch";
import { useToast } from "../context/ToastContext";
import { extractErrorMessage } from "../api/client";
import { CourseSidebar } from "../components/CourseSidebar";
import { LineSkeleton, ErrorState } from "../components/States";

export default function LessonReader() {
  const { courseId, lessonId } = useParams();
  const navigate = useNavigate();
  const { push } = useToast();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);
  const [completedIds, setCompletedIds] = useState(new Set());

  const courseFetch = useFetch(useCallback(() => coursesApi.get(courseId), [courseId]), [courseId]);

  const { flatLessons, lesson, module, lessonIndex } = useMemo(() => {
    if (!courseFetch.data) return { flatLessons: [], lesson: null, module: null, lessonIndex: -1 };
    const flat = [];
    for (const mod of courseFetch.data.modules) {
      for (const l of mod.lessons) flat.push({ ...l, moduleId: mod.id, moduleTitle: mod.title, quiz: mod.quiz });
    }
    const idx = flat.findIndex((l) => String(l.id) === String(lessonId));
    return { flatLessons: flat, lesson: flat[idx], module: courseFetch.data.modules.find((m) => m.id === flat[idx]?.moduleId), lessonIndex: idx };
  }, [courseFetch.data, lessonId]);

  if (courseFetch.isLoading) {
    return (
      <div className="max-w-3xl mx-auto px-5 py-10">
        <LineSkeleton className="w-1/3 mb-6" />
        <LineSkeleton className="w-2/3 h-8 mb-4" />
        <LineSkeleton className="w-full mb-2" />
        <LineSkeleton className="w-full mb-2" />
        <LineSkeleton className="w-4/5" />
      </div>
    );
  }
  if (courseFetch.error) {
    return <div className="max-w-3xl mx-auto px-5 py-10"><ErrorState description={courseFetch.error} onRetry={courseFetch.refetch} /></div>;
  }
  if (!lesson) {
    return <div className="max-w-3xl mx-auto px-5 py-10"><ErrorState title="Lesson not found" /></div>;
  }

  const course = courseFetch.data;
  const prevLesson = flatLessons[lessonIndex - 1];
  const nextLesson = flatLessons[lessonIndex + 1];
  const isLastInModule = !nextLesson || nextLesson.moduleId !== lesson.moduleId;

  async function handleMarkComplete() {
    setIsCompleting(true);
    try {
      const cert = await learningApi.completeLesson(lesson.id);
      setCompletedIds((prev) => new Set(prev).add(lesson.id));
      push("Lesson marked complete");
      if (cert) {
        confetti({ particleCount: 120, spread: 80, colors: ["#E8A33D", "#2E7D6B", "#F1F2EE"], origin: { y: 0.6 } });
        push(`Certificate earned for ${cert.course_title}! 🎉`);
      }
      if (isLastInModule && module?.quiz) {
        setTimeout(() => navigate(`/courses/${course.id}/quiz/${module.quiz.id}`), 700);
      } else if (nextLesson) {
        setTimeout(() => navigate(`/courses/${course.id}/learn/${nextLesson.id}`), 700);
      }
    } catch (err) {
      push(extractErrorMessage(err), "error");
    } finally {
      setIsCompleting(false);
    }
  }

  // merge fetched "already completed" state (module.completed count doesn't give ids,
  // so we infer from lesson list order is not reliable -- track locally per-visit instead,
  // and treat lessons before an already-in-progress point as done based on module counters).
  const completedFromServer = new Set();
  for (const mod of course.modules) {
    // best-effort: if this lesson index within module < completed_lessons, treat as done
    mod.lessons.forEach((l, i) => {
      if (i < mod.completed_lessons) completedFromServer.add(l.id);
    });
  }
  const allCompleted = new Set([...completedFromServer, ...completedIds]);

  return (
    <div className="flex">
      <CourseSidebar
        course={course}
        activeLessonId={lesson.id}
        completedLessonIds={allCompleted}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen((o) => !o)}
      />

      <main className="flex-1 min-w-0">
        <div className="max-w-3xl mx-auto px-5 py-10">
          <p className="text-xs text-mist mb-2">{lesson.moduleTitle}</p>
          <div className="flex items-start justify-between gap-4 mb-6">
            <h1 className="text-2xl font-display font-semibold leading-tight">{lesson.title}</h1>
            <span className="badge bg-white/5 text-mist text-[11px] shrink-0 mt-1">
              <Clock size={12} /> {lesson.estimated_minutes}m
            </span>
          </div>

          <article className="lesson-content">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{lesson.content}</ReactMarkdown>
          </article>

          <div className="flex items-center justify-between mt-10 pt-6 border-t border-white/5">
            {prevLesson ? (
              <Link to={`/courses/${course.id}/learn/${prevLesson.id}`} className="btn-secondary text-sm">
                <ChevronLeft size={15} /> Previous
              </Link>
            ) : <span />}

            {allCompleted.has(lesson.id) ? (
              <span className="flex items-center gap-2 text-sm text-teal-bright font-medium">
                <CheckCircle2 size={16} /> Completed
              </span>
            ) : (
              <button onClick={handleMarkComplete} disabled={isCompleting} className="btn-primary text-sm">
                <CheckCircle2 size={15} /> {isCompleting ? "Saving…" : "Mark complete"}
              </button>
            )}

            {nextLesson ? (
              <Link to={`/courses/${course.id}/learn/${nextLesson.id}`} className="btn-secondary text-sm">
                Next <ChevronRight size={15} />
              </Link>
            ) : module?.quiz ? (
              <Link to={`/courses/${course.id}/quiz/${module.quiz.id}`} className="btn-secondary text-sm">
                Module quiz <ChevronRight size={15} />
              </Link>
            ) : <span />}
          </div>
        </div>
      </main>
    </div>
  );
}
