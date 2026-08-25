import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { authApi } from "../api/resources";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadCurrentUser = useCallback(async () => {
    const token = localStorage.getItem("waypoint_token");
    if (!token) {
      setIsLoading(false);
      return;
    }
    try {
      const me = await authApi.me();
      setUser(me);
    } catch {
      localStorage.removeItem("waypoint_token");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCurrentUser();
  }, [loadCurrentUser]);

  async function login(email, password) {
    const data = await authApi.login({ email, password });
    localStorage.setItem("waypoint_token", data.access_token);
    setUser(data.user);
    return data.user;
  }

  async function register(payload) {
    const data = await authApi.register(payload);
    localStorage.setItem("waypoint_token", data.access_token);
    setUser(data.user);
    return data.user;
  }

  function logout() {
    localStorage.removeItem("waypoint_token");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, setUser, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
