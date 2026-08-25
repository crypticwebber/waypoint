import { Link } from "react-router-dom";
import { Compass, Target, Sparkles, GraduationCap, ArrowRight, MapPin } from "lucide-react";
import { RouteSteps } from "../components/RouteLine";

const journey = [
  { label: "Tell us your goal", state: "done" },
  { label: "Get matched to a path", state: "done" },
  { label: "Learn module by module", state: "current" },
  { label: "Earn your certificate", state: "upcoming" },
];

const categories = [
  { name: "Data Science", desc: "Python, pandas, and machine learning fundamentals", color: "#E8A33D" },
  { name: "Web Development", desc: "React and FastAPI, front to back", color: "#2E7D6B" },
  { name: "Cloud & DevOps", desc: "Docker, CI/CD, and real infrastructure concepts", color: "#5B4B8A" },
  { name: "Design", desc: "UX research, IA, and usability that holds up", color: "#B4507A" },
];

export default function Landing() {
  return (
    <div>
      {/* Hero */}
      <section className="max-w-7xl mx-auto px-5 pt-16 pb-20 md:pt-24 md:pb-28">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <span className="badge bg-white/5 text-mist mb-5">
              <MapPin size={13} /> Skills that go somewhere
            </span>
            <h1 className="text-4xl md:text-5xl font-display font-semibold leading-[1.1] mb-5">
              Learning that plots <span className="text-amber">a course</span>, not just a syllabus.
            </h1>
            <p className="text-lg text-mist leading-relaxed mb-8 max-w-lg">
              Waypoint asks what you're actually trying to get to, then builds your route:
              real courses, real projects, and recommendations that get sharper the more you learn.
            </p>
            <div className="flex flex-wrap items-center gap-3">
              <Link to="/register" className="btn-primary">
                Start your route <ArrowRight size={16} />
              </Link>
              <Link to="/catalog" className="btn-secondary">Browse courses</Link>
            </div>
          </div>

          <div className="card p-7">
            <p className="label mb-5">Your route</p>
            <RouteSteps steps={journey} />
            <div className="flex justify-between mt-2 mb-8">
              {journey.map((j, i) => (
                <span key={i} className={`text-[11px] max-w-[70px] text-center leading-tight ${j.state === "upcoming" ? "text-mist/60" : "text-mist"}`}>
                  {j.label}
                </span>
              ))}
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-3 p-3 rounded-xl bg-white/5">
                <div className="w-8 h-8 rounded-lg bg-teal/20 flex items-center justify-center text-teal-bright shrink-0">
                  <Sparkles size={15} />
                </div>
                <p className="text-sm text-paper/85">"Matches your interest in Data Science"</p>
              </div>
              <div className="flex items-center gap-3 p-3 rounded-xl bg-white/5">
                <div className="w-8 h-8 rounded-lg bg-amber/20 flex items-center justify-center text-amber shrink-0">
                  <Target size={15} />
                </div>
                <p className="text-sm text-paper/85">"Because you completed Python for Data Analysis"</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Waypoint */}
      <section className="max-w-7xl mx-auto px-5 py-16 border-t border-white/5">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <Compass size={22} className="text-amber mb-3" />
            <h3 className="font-display font-semibold text-lg mb-2">Recommendations from day one</h3>
            <p className="text-sm text-mist leading-relaxed">
              A two-minute survey gets you a real starting point immediately. No cold, empty
              dashboard waiting for you to "engage" first.
            </p>
          </div>
          <div>
            <GraduationCap size={22} className="text-teal-bright mb-3" />
            <h3 className="font-display font-semibold text-lg mb-2">Courses built to finish</h3>
            <p className="text-sm text-mist leading-relaxed">
              Module quizzes, hands-on projects, and a certificate that's actually earned --
              not just a completion badge for scrolling to the bottom.
            </p>
          </div>
          <div>
            <Sparkles size={22} className="text-amber mb-3" />
            <h3 className="font-display font-semibold text-lg mb-2">Gets sharper as you go</h3>
            <p className="text-sm text-mist leading-relaxed">
              Every lesson you finish quietly refines what we suggest next, blended with what
              you told us mattered to you in the first place.
            </p>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-7xl mx-auto px-5 py-16 border-t border-white/5">
        <h2 className="text-2xl font-display font-semibold mb-8">Pick a direction</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {categories.map((c) => (
            <Link
              key={c.name}
              to={`/catalog?category=${encodeURIComponent(c.name)}`}
              className="card p-5 hover:border-white/15 transition-colors group"
            >
              <span className="w-9 h-9 rounded-lg flex items-center justify-center mb-4" style={{ background: `${c.color}22` }}>
                <span className="route-dot !border-0" style={{ background: c.color }} />
              </span>
              <h3 className="font-display font-semibold mb-1.5 group-hover:text-amber transition-colors">{c.name}</h3>
              <p className="text-sm text-mist leading-relaxed">{c.desc}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-7xl mx-auto px-5 py-20 border-t border-white/5 text-center">
        <h2 className="text-3xl font-display font-semibold mb-4">Where are you trying to get to?</h2>
        <p className="text-mist mb-8 max-w-md mx-auto">Two minutes of setup. A route built around your answer, immediately.</p>
        <Link to="/register" className="btn-primary">
          Start your route <ArrowRight size={16} />
        </Link>
      </section>
    </div>
  );
}
