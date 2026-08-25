import { Link } from "react-router-dom";
import { CheckCircle2, Circle, FileQuestion, PanelLeftClose, PanelLeftOpen } from "lucide-react";

export function CourseSidebar({ course, activeLessonId, activeQuizId, completedLessonIds, isOpen, onToggle }) {
  return (
    <>
      <button
        onClick={onToggle}
        className="fixed top-20 left-4 z-40 md:hidden card p-2"
        aria-label={isOpen ? "Close syllabus" : "Open syllabus"}
      >
        {isOpen ? <PanelLeftClose size={18} /> : <PanelLeftOpen size={18} />}
      </button>

      <aside
        className={`fixed md:sticky top-16 h-[calc(100vh-4rem)] w-72 shrink-0 border-r border-white/5 bg-ink overflow-y-auto z-30 transition-transform md:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="p-4">
          <Link to={`/courses/${course.id}`} className="text-xs text-mist hover:text-paper mb-3 block">&larr; {course.title}</Link>
          {course.modules.map((mod, mi) => (
            <div key={mod.id} className="mb-4">
              <p className="text-xs font-mono text-mist mb-1.5 px-1">
                {String(mi + 1).padStart(2, "0")} · {mod.title}
              </p>
              <ul className="space-y-0.5">
                {mod.lessons.map((lesson) => {
                  const isDone = completedLessonIds.has(lesson.id);
                  const isActive = lesson.id === activeLessonId;
                  return (
                    <li key={lesson.id}>
                      <Link
                        to={`/courses/${course.id}/learn/${lesson.id}`}
                        className={`flex items-center gap-2 px-2.5 py-2 rounded-lg text-sm transition-colors ${
                          isActive ? "bg-amber/10 text-amber" : "text-paper/75 hover:bg-white/5"
                        }`}
                      >
                        {isDone ? (
                          <CheckCircle2 size={14} className="text-teal-bright shrink-0" />
                        ) : (
                          <Circle size={14} className="text-mist shrink-0" />
                        )}
                        <span className="truncate">{lesson.title}</span>
                      </Link>
                    </li>
                  );
                })}
                {mod.quiz && (
                  <li>
                    <Link
                      to={`/courses/${course.id}/quiz/${mod.quiz.id}`}
                      className={`flex items-center gap-2 px-2.5 py-2 rounded-lg text-sm transition-colors ${
                        mod.quiz.id === activeQuizId ? "bg-amber/10 text-amber" : "text-paper/75 hover:bg-white/5"
                      }`}
                    >
                      <FileQuestion size={14} className={mod.quiz.best_score != null ? "text-teal-bright shrink-0" : "text-mist shrink-0"} />
                      <span className="truncate">{mod.quiz.title}</span>
                      {mod.quiz.best_score != null && <span className="ml-auto text-xs font-mono shrink-0">{mod.quiz.best_score}%</span>}
                    </Link>
                  </li>
                )}
              </ul>
            </div>
          ))}
        </div>
      </aside>
    </>
  );
}
