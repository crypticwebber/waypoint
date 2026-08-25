/**
 * The Waypoint "route line" -- a dotted path with circular markers.
 * This is the product's one signature visual element, reused consistently
 * as a progress bar (percent-filled route to a destination), and as a
 * lightweight sequence indicator for a list of steps/modules. Colors
 * intentionally echo the certificate PDF's route-line flourish.
 */
export function RouteProgress({ percent = 0, label, showPercent = true }) {
  const clamped = Math.max(0, Math.min(100, percent));
  return (
    <div className="w-full">
      {(label || showPercent) && (
        <div className="flex items-center justify-between mb-1.5">
          {label && <span className="label">{label}</span>}
          {showPercent && <span className="text-xs font-mono text-mist">{Math.round(clamped)}%</span>}
        </div>
      )}
      <div className="route-line">
        <div className="route-line-fill" style={{ width: `${clamped}%` }} />
      </div>
    </div>
  );
}

export function RouteSteps({ steps }) {
  // steps: [{ label, state: 'done' | 'current' | 'upcoming' }]
  return (
    <div className="flex items-center w-full">
      {steps.map((step, i) => (
        <div key={i} className="flex items-center flex-1 last:flex-initial">
          <div
            className="route-dot"
            style={{
              background:
                step.state === "done" ? "#2E7D6B" : step.state === "current" ? "#E8A33D" : "#3a4650",
            }}
            title={step.label}
          />
          {i < steps.length - 1 && (
            <div
              className="flex-1 h-[2px] mx-1"
              style={{ background: step.state === "done" ? "#2E7D6B" : "#3a4650" }}
            />
          )}
        </div>
      ))}
    </div>
  );
}
