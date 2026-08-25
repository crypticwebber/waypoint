import { useCallback, useEffect, useState } from "react";
import { extractErrorMessage } from "../api/client";

/**
 * Small shared hook so every screen handles loading/error/success the same
 * way instead of re-implementing it. `fn` should be a stable callback
 * (wrap with useCallback at the call site) that returns a promise.
 */
export function useFetch(fn, deps = []) {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const run = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await fn();
      setData(result);
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    run();
  }, [run]);

  return { data, isLoading, error, refetch: run, setData };
}
