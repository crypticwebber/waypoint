import { createContext, useCallback, useContext, useState } from "react";
import { CheckCircle2, AlertCircle, Info, X } from "lucide-react";

const ToastContext = createContext(null);

let idCounter = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const dismiss = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const push = useCallback((message, variant = "success") => {
    const id = ++idCounter;
    setToasts((prev) => [...prev, { id, message, variant }]);
    setTimeout(() => dismiss(id), 4200);
  }, [dismiss]);

  return (
    <ToastContext.Provider value={{ push }}>
      {children}
      <div className="fixed bottom-5 right-5 z-[100] flex flex-col gap-2 w-[calc(100%-2.5rem)] max-w-sm">
        {toasts.map((t) => (
          <div
            key={t.id}
            role="status"
            className="card flex items-start gap-3 px-4 py-3 shadow-2xl shadow-black/40 animate-[fadein_0.2s_ease]"
          >
            {t.variant === "success" && <CheckCircle2 size={18} className="text-teal-bright mt-0.5 shrink-0" />}
            {t.variant === "error" && <AlertCircle size={18} className="text-coral mt-0.5 shrink-0" />}
            {t.variant === "info" && <Info size={18} className="text-amber mt-0.5 shrink-0" />}
            <p className="text-sm text-paper/90 flex-1">{t.message}</p>
            <button onClick={() => dismiss(t.id)} aria-label="Dismiss notification" className="text-mist hover:text-paper shrink-0">
              <X size={16} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within ToastProvider");
  return ctx;
}
