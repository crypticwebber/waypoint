import { AlertTriangle, Compass, RotateCw } from "lucide-react";

export function CardSkeleton() {
  return (
    <div className="card p-5">
      <div className="skeleton h-4 w-20 mb-4" />
      <div className="skeleton h-5 w-4/5 mb-2" />
      <div className="skeleton h-4 w-full mb-1.5" />
      <div className="skeleton h-4 w-3/4 mb-4" />
      <div className="skeleton h-2 w-full" />
    </div>
  );
}

export function CardGridSkeleton({ count = 6 }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      {Array.from({ length: count }).map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  );
}

export function LineSkeleton({ className = "" }) {
  return <div className={`skeleton h-4 ${className}`} />;
}

export function EmptyState({ icon: Icon = Compass, title, description, action }) {
  return (
    <div className="text-center py-16 px-6">
      <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-white/5 mb-4">
        <Icon size={26} className="text-mist" />
      </div>
      <h3 className="font-display text-lg font-semibold mb-1.5">{title}</h3>
      {description && <p className="text-mist text-sm max-w-sm mx-auto mb-5">{description}</p>}
      {action}
    </div>
  );
}

export function ErrorState({ title = "Something went wrong", description, onRetry }) {
  return (
    <div className="text-center py-16 px-6">
      <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-coral/10 mb-4">
        <AlertTriangle size={26} className="text-coral" />
      </div>
      <h3 className="font-display text-lg font-semibold mb-1.5">{title}</h3>
      {description && <p className="text-mist text-sm max-w-sm mx-auto mb-5">{description}</p>}
      {onRetry && (
        <button onClick={onRetry} className="btn-secondary">
          <RotateCw size={16} /> Try again
        </button>
      )}
    </div>
  );
}
