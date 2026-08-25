import { Link, NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";
import { Compass, LayoutDashboard, LibraryBig, GraduationCap, Menu, X, LogOut, ChevronDown } from "lucide-react";
import { useAuth } from "../context/AuthContext";

function Logo() {
  return (
    <Link to="/" className="flex items-center gap-2 shrink-0 group">
      <span className="relative flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-teal to-amber">
        <Compass size={16} className="text-ink" strokeWidth={2.5} />
      </span>
      <span className="font-display font-semibold text-lg tracking-tight">Waypoint</span>
    </Link>
  );
}

const studentLinks = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/catalog", label: "Catalog", icon: LibraryBig },
  { to: "/certificates", label: "Certificates", icon: GraduationCap },
];

export function Nav() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  function handleLogout() {
    logout();
    navigate("/");
  }

  const links = user?.role === "instructor"
    ? [{ to: "/instructor", label: "Instructor Studio", icon: LayoutDashboard }]
    : studentLinks;

  return (
    <header className="sticky top-0 z-50 bg-ink/90 backdrop-blur border-b border-white/5">
      <div className="max-w-7xl mx-auto px-5 h-16 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Logo />
          {user && (
            <nav className="hidden md:flex items-center gap-1">
              {links.map((l) => (
                <NavLink
                  key={l.to}
                  to={l.to}
                  className={({ isActive }) =>
                    `flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      isActive ? "bg-white/10 text-paper" : "text-mist hover:text-paper hover:bg-white/5"
                    }`
                  }
                >
                  <l.icon size={16} /> {l.label}
                </NavLink>
              ))}
            </nav>
          )}
        </div>

        <div className="hidden md:flex items-center gap-3">
          {user ? (
            <div className="relative">
              <button
                onClick={() => setMenuOpen((o) => !o)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-full hover:bg-white/5 transition-colors"
              >
                <span className="w-7 h-7 rounded-full bg-teal/30 text-teal-bright flex items-center justify-center text-xs font-semibold font-display">
                  {user.full_name.slice(0, 1).toUpperCase()}
                </span>
                <span className="text-sm text-paper/90">{user.full_name}</span>
                <ChevronDown size={14} className="text-mist" />
              </button>
              {menuOpen && (
                <div
                  className="absolute right-0 mt-2 w-44 card p-1.5 shadow-xl"
                  onMouseLeave={() => setMenuOpen(false)}
                >
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-coral hover:bg-coral/10 transition-colors"
                  >
                    <LogOut size={15} /> Log out
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <Link to="/login" className="btn-ghost text-sm">Log in</Link>
              <Link to="/register" className="btn-primary text-sm">Get started</Link>
            </>
          )}
        </div>

        <button className="md:hidden text-paper" onClick={() => setMobileOpen((o) => !o)} aria-label="Toggle menu">
          {mobileOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {mobileOpen && (
        <div className="md:hidden border-t border-white/5 px-5 py-3 flex flex-col gap-1">
          {user ? (
            <>
              {links.map((l) => (
                <NavLink
                  key={l.to}
                  to={l.to}
                  onClick={() => setMobileOpen(false)}
                  className="flex items-center gap-2 px-3 py-2.5 rounded-lg text-sm font-medium text-paper/90 hover:bg-white/5"
                >
                  <l.icon size={16} /> {l.label}
                </NavLink>
              ))}
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-3 py-2.5 rounded-lg text-sm text-coral hover:bg-coral/10 text-left"
              >
                <LogOut size={15} /> Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" onClick={() => setMobileOpen(false)} className="px-3 py-2.5 text-sm text-paper/90">Log in</Link>
              <Link to="/register" onClick={() => setMobileOpen(false)} className="px-3 py-2.5 text-sm font-semibold text-amber">Get started</Link>
            </>
          )}
        </div>
      )}
    </header>
  );
}
