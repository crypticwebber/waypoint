import { useCallback, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Plus, Trash2, ChevronDown, ChevronUp } from "lucide-react";
import { coursesApi, instructorApi } from "../api/resources";
import { useFetch } from "../hooks/useFetch";
import { useToast } from "../context/ToastContext";
import { extractErrorMessage } from "../api/client";
import { ErrorState, LineSkeleton } from "../components/States";

export default function InstructorCourseEditor() {
  const { courseId } = useParams();
  const { push } = useToast();
  const courseFetch = useFetch(useCallback(() => coursesApi.get(courseId), [courseId]), [courseId]);
  const [openModule, setOpenModule] = useState(null);
  const [newModuleTitle, setNewModuleTitle] = useState("");

  async function handleAddModule(e) {
    e.preventDefault();
    if (!newModuleTitle.trim()) return;
    try {
      await instructorApi.createModule(courseId, { title: newModuleTitle, order: (courseFetch.data?.modules.length || 0) });
      setNewModuleTitle("");
      push("Module added");
      courseFetch.refetch();
    } catch (err) {
      push(extractErrorMessage(err), "error");
    }
  }

  async function handleDeleteModule(moduleId) {
    if (!confirm("Delete this module and everything in it?")) return;
    try {
      await instructorApi.deleteModule(moduleId);
      push("Module deleted");
      courseFetch.refetch();
    } catch (err) {
      push(extractErrorMessage(err), "error");
    }
  }

  if (courseFetch.isLoading) {
    return <div className="max-w-3xl mx-auto px-5 py-10"><LineSkeleton className="w-1/2 h-8 mb-4" /><LineSkeleton className="w-full h-40" /></div>;
  }
  if (courseFetch.error) {
    return <div className="max-w-3xl mx-auto px-5 py-10"><ErrorState description={courseFetch.error} onRetry={courseFetch.refetch} /></div>;
  }

  const course = courseFetch.data;

  return (
    <div className="max-w-3xl mx-auto px-5 py-10">
      <Link to="/instructor" className="flex items-center gap-1.5 text-sm text-mist hover:text-paper mb-6">
        <ArrowLeft size={15} /> Back to studio
      </Link>
      <h1 className="text-2xl font-display font-semibold mb-1">{course.title}</h1>
      <p className="text-mist mb-8">Manage modules, lessons, and quizzes.</p>

      <div className="space-y-3 mb-6">
        {course.modules.map((mod, i) => (
          <ModuleEditor
            key={mod.id}
            module={mod}
            index={i}
            isOpen={openModule === mod.id}
            onToggle={() => setOpenModule(openModule === mod.id ? null : mod.id)}
            onDelete={() => handleDeleteModule(mod.id)}
            onChanged={courseFetch.refetch}
          />
        ))}
      </div>

      <form onSubmit={handleAddModule} className="card p-4 flex gap-2">
        <input
          className="input" placeholder="New module title"
          value={newModuleTitle} onChange={(e) => setNewModuleTitle(e.target.value)}
        />
        <button type="submit" className="btn-primary text-sm shrink-0"><Plus size={15} /> Add module</button>
      </form>
    </div>
  );
}

function ModuleEditor({ module, index, isOpen, onToggle, onDelete, onChanged }) {
  const { push } = useToast();
  const [newLessonTitle, setNewLessonTitle] = useState("");
  const [newLessonContent, setNewLessonContent] = useState("");

  async function handleAddLesson(e) {
    e.preventDefault();
    if (!newLessonTitle.trim() || !newLessonContent.trim()) return;
    try {
      await instructorApi.createLesson(module.id, {
        title: newLessonTitle, content: newLessonContent, order: module.lessons.length, estimated_minutes: 10,
      });
      setNewLessonTitle(""); setNewLessonContent("");
      push("Lesson added");
      onChanged();
    } catch (err) {
      push(extractErrorMessage(err), "error");
    }
  }

  async function handleDeleteLesson(lessonId) {
    if (!confirm("Delete this lesson?")) return;
    try {
      await instructorApi.deleteLesson(lessonId);
      push("Lesson deleted");
      onChanged();
    } catch (err) {
      push(extractErrorMessage(err), "error");
    }
  }

  async function handleCreateQuiz() {
    try {
      await instructorApi.createQuiz(module.id, `${module.title} Check`);
      push("Quiz created -- add questions below");
      onChanged();
    } catch (err) {
      push(extractErrorMessage(err), "error");
    }
  }

  return (
    <div className="card overflow-hidden">
      <div className="flex items-center justify-between px-5 py-4">
        <button onClick={onToggle} className="flex items-center gap-3 min-w-0 flex-1 text-left" aria-expanded={isOpen}>
          <span className="font-mono text-xs text-mist shrink-0">{String(index + 1).padStart(2, "0")}</span>
          <span className="font-medium text-sm truncate">{module.title}</span>
          <span className="text-xs text-mist shrink-0">({module.lessons.length} lessons{module.quiz ? ", quiz set" : ""})</span>
        </button>
        <div className="flex items-center gap-1 shrink-0">
          <button onClick={onDelete} aria-label="Delete module" className="text-mist hover:text-coral p-1.5"><Trash2 size={15} /></button>
          <button onClick={onToggle} aria-label="Toggle module">{isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}</button>
        </div>
      </div>

      {isOpen && (
        <div className="px-5 pb-5 border-t border-white/5 pt-4 space-y-4">
          <div className="space-y-2">
            {module.lessons.map((lesson) => (
              <div key={lesson.id} className="flex items-center justify-between bg-white/5 rounded-lg px-3 py-2">
                <span className="text-sm text-paper/85 truncate">{lesson.title}</span>
                <button onClick={() => handleDeleteLesson(lesson.id)} aria-label="Delete lesson" className="text-mist hover:text-coral shrink-0"><Trash2 size={14} /></button>
              </div>
            ))}
            {module.lessons.length === 0 && <p className="text-xs text-mist">No lessons yet.</p>}
          </div>

          <form onSubmit={handleAddLesson} className="space-y-2 bg-white/5 rounded-xl p-3">
            <p className="label">Add lesson</p>
            <input className="input" placeholder="Lesson title" value={newLessonTitle} onChange={(e) => setNewLessonTitle(e.target.value)} />
            <textarea className="input min-h-[90px]" placeholder="Lesson content (markdown supported)" value={newLessonContent} onChange={(e) => setNewLessonContent(e.target.value)} />
            <button type="submit" className="btn-secondary text-sm"><Plus size={14} /> Add lesson</button>
          </form>

          <div className="border-t border-white/5 pt-4">
            <p className="label mb-2">Quiz</p>
            {module.quiz ? (
              <QuizEditor quiz={module.quiz} onChanged={onChanged} />
            ) : (
              <button onClick={handleCreateQuiz} className="btn-secondary text-sm"><Plus size={14} /> Create quiz for this module</button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function QuizEditor({ quiz, onChanged }) {
  const { push } = useToast();
  const [form, setForm] = useState({ question_text: "", options: ["", "", "", ""], correct_index: 0 });

  async function handleAddQuestion(e) {
    e.preventDefault();
    const options = form.options.map((o) => o.trim()).filter(Boolean);
    if (!form.question_text.trim() || options.length < 2) {
      push("Add a question and at least two options", "error");
      return;
    }
    try {
      await instructorApi.addQuestion(quiz.id, { question_text: form.question_text, options, correct_index: form.correct_index });
      setForm({ question_text: "", options: ["", "", "", ""], correct_index: 0 });
      push("Question added");
      onChanged();
    } catch (err) {
      push(extractErrorMessage(err), "error");
    }
  }

  async function handleDeleteQuestion(questionId) {
    try {
      await instructorApi.deleteQuestion(questionId);
      push("Question deleted");
      onChanged();
    } catch (err) {
      push(extractErrorMessage(err), "error");
    }
  }

  return (
    <div className="space-y-3">
      <div className="space-y-2">
        {quiz.questions.map((q, i) => (
          <div key={q.id} className="bg-white/5 rounded-lg px-3 py-2 flex items-start justify-between gap-3">
            <div className="min-w-0">
              <p className="text-sm text-paper/85">{i + 1}. {q.question_text}</p>
              <p className="text-xs text-mist mt-1">{q.options.length} options</p>
            </div>
            <button onClick={() => handleDeleteQuestion(q.id)} aria-label="Delete question" className="text-mist hover:text-coral shrink-0"><Trash2 size={14} /></button>
          </div>
        ))}
        {quiz.questions.length === 0 && <p className="text-xs text-mist">No questions yet.</p>}
      </div>

      <form onSubmit={handleAddQuestion} className="space-y-2 bg-white/5 rounded-xl p-3">
        <p className="label">Add question</p>
        <input className="input" placeholder="Question text" value={form.question_text} onChange={(e) => setForm((f) => ({ ...f, question_text: e.target.value }))} />
        {form.options.map((opt, i) => (
          <div key={i} className="flex items-center gap-2">
            <input
              type="radio" name="correct" checked={form.correct_index === i}
              onChange={() => setForm((f) => ({ ...f, correct_index: i }))}
              className="accent-amber shrink-0" aria-label={`Mark option ${i + 1} as correct`}
            />
            <input
              className="input" placeholder={`Option ${i + 1}`} value={opt}
              onChange={(e) => setForm((f) => { const options = [...f.options]; options[i] = e.target.value; return { ...f, options }; })}
            />
          </div>
        ))}
        <p className="text-xs text-mist">Select the radio button next to the correct option.</p>
        <button type="submit" className="btn-secondary text-sm"><Plus size={14} /> Add question</button>
      </form>
    </div>
  );
}
