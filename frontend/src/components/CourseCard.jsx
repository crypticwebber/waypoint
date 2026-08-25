import { Link } from "react-router-dom";
import { Star, Users, Clock } from "lucide-react";

const LEVEL_LABEL = { beginner: "Beginner", intermediate: "Intermediate", advanced: "Advanced" };

export function CourseCard({ course, reason }) {
  return (
    <Link
      to={`/courses/${course.id}`}
      className="card p-5 flex flex-col hover:border-white/15 transition-colors group"
    >
      <div className="flex items-center justify-between mb-4">
        <span
          className="badge font-mono text-[11px]"
          style={{ background: `${course.color}22`, color: course.color }}
        >
          {course.category}
        </span>
        <span className="badge bg-white/5 text-mist text-[11px]">{LEVEL_LABEL[course.level]}</span>
      </div>

      <h3 className="font-display font-semibold text-base mb-1.5 leading-snug group-hover:text-amber transition-colors">
        {course.title}
      </h3>
      <p className="text-sm text-mist leading-relaxed mb-4 line-clamp-3">{course.description}</p>

      {reason && (
        <p className="text-xs text-teal-bright mb-3 flex items-center gap-1.5">
          <span className="route-dot !w-1.5 !h-1.5 !border-0 bg-teal-bright" /> {reason}
        </p>
      )}

      <div className="mt-auto flex items-center justify-between pt-4 border-t border-white/5 text-xs text-mist">
        <span className="flex items-center gap-1"><Clock size={13} /> {course.duration_hours}h</span>
        <span className="flex items-center gap-1"><Users size={13} /> {course.enrolled_count}</span>
        <span className="flex items-center gap-1">
          <Star size={13} className={course.avg_rating ? "text-amber fill-amber" : ""} />
          {course.avg_rating ? course.avg_rating.toFixed(1) : "New"}
        </span>
      </div>
    </Link>
  );
}
