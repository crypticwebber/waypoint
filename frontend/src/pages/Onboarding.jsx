import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight, ArrowLeft, Sparkles } from "lucide-react";
import { coursesApi, preferencesApi, recommendationsApi } from "../api/resources";
import { extractErrorMessage } from "../api/client";
import { RouteSteps } from "../components/RouteLine";
import { CourseCard } from "../components/CourseCard";
import { CardGridSkeleton } from "../components/States";
import { useToast } from "../context/ToastContext";

const GOALS = [
  { value: "career_change", label: "Career change", desc: "Moving into a new field entirely" },
  { value: "upskilling", label: "Upskilling", desc: "Getting better at my current job" },
  { value: "academic", label: "Academic", desc: "Coursework or research" },
  { value: "personal_interest", label: "Personal interest", desc: "Just curious, no particular goal" },
];

const LEVELS = [
  { value: "beginner", label: "Beginner", desc: "New to this area" },
  { value: "intermediate", label: "Intermediate", desc: "Comfortable with the basics" },
  { value: "advanced", label: "Advanced", desc: "Deep experience already" },
];

export default function Onboarding() {
  const navigate = useNavigate();
  const { push } = useToast();
  const [step, setStep] = useState(0); // 0..3, 4 = results
  const [categories, setCategories] = useState([]);
  const [interests, setInterests] = useState([]);
  const [skillLevel, setSkillLevel] = useState(null);
  const [goal, setGoal] = useState(null);
  const [freeText, setFreeText] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [recommendations, setRecommendations] = useState(null);

  useEffect(() => {
    coursesApi.categories().then(setCategories).catch(() => setCategories([]));
  }, []);

  function toggleInterest(cat) {
    setInterests((prev) => (prev.includes(cat) ? prev.filter((c) => c !== cat) : [...prev, cat]));
  }

  async function finish() {
    setIsSubmitting(true);
    setError(null);
    try {
      await preferencesApi.save({
        interests, skill_level: skillLevel, goal, free_text_interest: freeText || null,
      });
      const recs = await recommendationsApi.mine(6);
      setRecommendations(recs);
      setStep(4);
      push("Preferences saved -- here's your starting point");
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  }

  const steps = [
    { label: "Interests", state: step > 0 ? "done" : "current" },
    { label: "Skill level", state: step > 1 ? "done" : step === 1 ? "current" : "upcoming" },
    { label: "Goal", state: step > 2 ? "done" : step === 2 ? "current" : "upcoming" },
    { label: "Details", state: step > 3 ? "done" : step === 3 ? "current" : "upcoming" },
  ];

  if (step === 4) {
    return (
      <div className="max-w-5xl mx-auto px-5 py-14">
        <div className="text-center mb-10">
          <span className="badge bg-teal/15 text-teal-bright mb-4"><Sparkles size={13} /> Built from your answers</span>
          <h1 className="text-3xl font-display font-semibold mb-2">Your starting route</h1>
          <p className="text-mist">This is 100% based on what you just told us -- it'll sharpen as you start learning.</p>
        </div>
        {!recommendations ? (
          <CardGridSkeleton count={6} />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mb-10">
            {recommendations.map((r) => (
              <CourseCard key={r.course.id} course={r.course} reason={r.reason} />
            ))}
          </div>
        )}
        <div className="text-center">
          <button onClick={() => navigate("/dashboard")} className="btn-primary">
            Go to my dashboard <ArrowRight size={16} />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto px-5 py-14">
      <div className="mb-10">
        <RouteSteps steps={steps} />
        <div className="flex justify-between mt-2">
          {steps.map((s, i) => (
            <span key={i} className={`text-[11px] ${s.state === "upcoming" ? "text-mist/50" : "text-mist"}`}>{s.label}</span>
          ))}
        </div>
      </div>

      {error && (
        <div role="alert" className="bg-coral/10 border border-coral/30 text-coral text-sm rounded-xl px-4 py-3 mb-5">
          {error}
        </div>
      )}

      {step === 0 && (
        <StepCard
          title="What are you interested in?"
          description="Pick as many as you like -- this drives your very first recommendations."
        >
          <div className="grid grid-cols-2 gap-2.5">
            {(categories.length ? categories : ["Data Science", "Web Development", "Cloud & DevOps", "Design"]).map((cat) => (
              <button
                key={cat} type="button" onClick={() => toggleInterest(cat)}
                className={`rounded-xl border px-4 py-3 text-sm font-medium text-left transition-colors ${
                  interests.includes(cat) ? "border-amber bg-amber/10 text-amber" : "border-white/10 text-paper/80 hover:border-white/25"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
          <NavButtons onNext={() => setStep(1)} nextDisabled={interests.length === 0} />
        </StepCard>
      )}

      {step === 1 && (
        <StepCard title="What's your current skill level?" description="Be honest -- we'll match course difficulty to this.">
          <div className="space-y-2.5">
            {LEVELS.map((lvl) => (
              <button
                key={lvl.value} type="button" onClick={() => setSkillLevel(lvl.value)}
                className={`w-full rounded-xl border px-4 py-3 text-left transition-colors ${
                  skillLevel === lvl.value ? "border-amber bg-amber/10" : "border-white/10 hover:border-white/25"
                }`}
              >
                <div className={`font-medium text-sm ${skillLevel === lvl.value ? "text-amber" : "text-paper"}`}>{lvl.label}</div>
                <div className="text-xs text-mist mt-0.5">{lvl.desc}</div>
              </button>
            ))}
          </div>
          <NavButtons onBack={() => setStep(0)} onNext={() => setStep(2)} nextDisabled={!skillLevel} />
        </StepCard>
      )}

      {step === 2 && (
        <StepCard title="What's your goal?" description="This keeps mattering even once you've got a learning history.">
          <div className="space-y-2.5">
            {GOALS.map((g) => (
              <button
                key={g.value} type="button" onClick={() => setGoal(g.value)}
                className={`w-full rounded-xl border px-4 py-3 text-left transition-colors ${
                  goal === g.value ? "border-amber bg-amber/10" : "border-white/10 hover:border-white/25"
                }`}
              >
                <div className={`font-medium text-sm ${goal === g.value ? "text-amber" : "text-paper"}`}>{g.label}</div>
                <div className="text-xs text-mist mt-0.5">{g.desc}</div>
              </button>
            ))}
          </div>
          <NavButtons onBack={() => setStep(1)} onNext={() => setStep(3)} nextDisabled={!goal} />
        </StepCard>
      )}

      {step === 3 && (
        <StepCard title="Anything more specific?" description="Optional -- a sentence is plenty. This gets matched directly against course descriptions.">
          <textarea
            className="input min-h-[110px] resize-none"
            placeholder="e.g. I want to get better at analyzing data and eventually move into machine learning"
            value={freeText}
            onChange={(e) => setFreeText(e.target.value)}
            maxLength={400}
          />
          <NavButtons onBack={() => setStep(2)} onNext={finish} nextLabel={isSubmitting ? "Building your route…" : "See my recommendations"} nextDisabled={isSubmitting} />
        </StepCard>
      )}
    </div>
  );
}

function StepCard({ title, description, children }) {
  return (
    <div className="card p-7">
      <h2 className="font-display font-semibold text-xl mb-1.5">{title}</h2>
      <p className="text-sm text-mist mb-6">{description}</p>
      {children}
    </div>
  );
}

function NavButtons({ onBack, onNext, nextDisabled, nextLabel = "Continue" }) {
  return (
    <div className="flex items-center justify-between mt-7">
      {onBack ? (
        <button type="button" onClick={onBack} className="btn-ghost text-sm"><ArrowLeft size={15} /> Back</button>
      ) : <span />}
      <button type="button" onClick={onNext} disabled={nextDisabled} className="btn-primary text-sm">
        {nextLabel} <ArrowRight size={15} />
      </button>
    </div>
  );
}
