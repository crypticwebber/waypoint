import { useCallback, useMemo, useState } from "react";
import { useParams, Link } from "react-router-dom";
import confetti from "canvas-confetti";
import { CheckCircle2, XCircle, RotateCw, ChevronRight, History } from "lucide-react";
import { coursesApi, learningApi } from "../api/resources";
import { useFetch } from "../hooks/useFetch";
import { useToast } from "../context/ToastContext";
import { extractErrorMessage } from "../api/client";
import { CourseSidebar } from "../components/CourseSidebar";
import { LineSkeleton, ErrorState } from "../components/States";

export default function Quiz() {
  const { courseId, quizId } = useParams();
  const { push } = useToast();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null); // { score, correctByQuestion }
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  const courseFetch = useFetch(useCallback(() => coursesApi.get(courseId), [courseId]), [courseId]);
  const historyFetch = useFetch(useCallback(() => learningApi.quizHistory(quizId), [quizId]), [quizId]);

  const { quiz, module } = useMemo(() => {
    if (!courseFetch.data) return { quiz: null, module: null };
    for (const mod of courseFetch.data.modules) {
      if (mod.quiz && String(mod.quiz.id) === String(quizId)) return { quiz: mod.quiz, module: mod };
    }
    return { quiz: null, module: null };
  }, [courseFetch.data, quizId]);

  if (courseFetch.isLoading) {
    return <div className="max-w-2xl mx-auto px-5 py-10"><LineSkeleton className="w-2/3 h-8 mb-4" /><LineSkeleton className="w-full h-40" /></div>;
  }
  if (courseFetch.error) {
    return <div className="max-w-2xl mx-auto px-5 py-10"><ErrorState description={courseFetch.error} onRetry={courseFetch.refetch} /></div>;
  }
  if (!quiz) {
    return <div className="max-w-2xl mx-auto px-5 py-10"><ErrorState title="Quiz not found" /></div>;
  }

  const course = courseFetch.data;
  const allAnswered = quiz.questions.every((q) => answers[q.id] != null);

  async function handleSubmit() {
    setIsSubmitting(true);
    try {
      const orderedAnswers = quiz.questions.map((q) => answers[q.id]);
      const attempt = await learningApi.submitQuiz(quiz.id, orderedAnswers);
      setResult({ score: attempt.score });
      historyFetch.refetch();
      if (attempt.score >= 70) {
        confetti({ particleCount: 90, spread: 70, colors: ["#E8A33D", "#2E7D6B"], origin: { y: 0.6 } });
        push(`Nice -- you scored ${attempt.score}%`);
      } else {
        push(`Scored ${attempt.score}% -- worth a retake once you review`, "info");
      }
    } catch (err) {
      push(extractErrorMessage(err), "error");
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleRetake() {
    setAnswers({});
    setResult(null);
  }

  const completedFromServer = new Set();
  for (const mod of course.modules) {
    mod.lessons.forEach((l, i) => { if (i < mod.completed_lessons) completedFromServer.add(l.id); });
  }

  return (
    <div className="flex">
      <CourseSidebar
        course={course}
        activeQuizId={quiz.id}
        completedLessonIds={completedFromServer}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen((o) => !o)}
      />

      <main className="flex-1 min-w-0">
        <div className="max-w-2xl mx-auto px-5 py-10">
          <p className="text-xs text-mist mb-2">{module.title}</p>
          <div className="flex items-start justify-between gap-4 mb-2">
            <h1 className="text-2xl font-display font-semibold leading-tight">{quiz.title}</h1>
          </div>
          <button onClick={() => setShowHistory((s) => !s)} className="flex items-center gap-1.5 text-xs text-mist hover:text-paper mb-6">
            <History size={13} /> {quiz.best_score != null ? `Best score: ${quiz.best_score}%` : "No attempts yet"} · {quiz.attempt_count} attempt{quiz.attempt_count === 1 ? "" : "s"}
          </button>

          {showHistory && historyFetch.data && (
            <div className="card p-4 mb-6">
              <p className="label mb-2">Attempt history</p>
              <ul className="space-y-1.5">
                {historyFetch.data.map((a) => (
                  <li key={a.id} className="flex items-center justify-between text-sm">
                    <span className="text-mist">{new Date(a.taken_at).toLocaleString()}</span>
                    <span className={a.score >= 70 ? "text-teal-bright font-mono" : "text-coral font-mono"}>{a.score}%</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {result ? (
            <div className="card p-7 text-center">
              <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full mb-4 ${result.score >= 70 ? "bg-teal/15" : "bg-coral/15"}`}>
                {result.score >= 70 ? <CheckCircle2 size={30} className="text-teal-bright" /> : <XCircle size={30} className="text-coral" />}
              </div>
              <h2 className="text-2xl font-display font-semibold mb-1">{result.score}%</h2>
              <p className="text-sm text-mist mb-6">
                {result.score >= 70 ? "Passed -- nice work." : "Below the 70% pass threshold -- review and try again."}
              </p>
              <div className="flex items-center justify-center gap-3">
                <button onClick={handleRetake} className="btn-secondary text-sm"><RotateCw size={15} /> Retake quiz</button>
                <Link to={`/courses/${course.id}`} className="btn-primary text-sm">Back to course <ChevronRight size={15} /></Link>
              </div>
            </div>
          ) : (
            <div className="space-y-5">
              {quiz.questions.map((q, qi) => (
                <fieldset key={q.id} className="card p-5">
                  <legend className="text-sm font-medium mb-3 px-1">{qi + 1}. {q.question_text}</legend>
                  <div className="space-y-2">
                    {q.options.map((opt, oi) => (
                      <label
                        key={oi}
                        className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl border text-sm cursor-pointer transition-colors ${
                          answers[q.id] === oi ? "border-amber bg-amber/10 text-amber" : "border-white/10 text-paper/85 hover:border-white/25"
                        }`}
                      >
                        <input
                          type="radio" name={`q-${q.id}`} className="accent-amber"
                          checked={answers[q.id] === oi}
                          onChange={() => setAnswers((a) => ({ ...a, [q.id]: oi }))}
                        />
                        {opt}
                      </label>
                    ))}
                  </div>
                </fieldset>
              ))}
              <button onClick={handleSubmit} disabled={!allAnswered || isSubmitting} className="btn-primary w-full">
                {isSubmitting ? "Scoring…" : "Submit answers"}
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
