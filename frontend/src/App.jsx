import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ToastProvider } from "./context/ToastContext";
import { RequireAuth, RequireInstructor } from "./components/RouteGuards";
import { Nav } from "./components/Nav";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Onboarding from "./pages/Onboarding";
import Dashboard from "./pages/Dashboard";
import Catalog from "./pages/Catalog";
import CourseDetail from "./pages/CourseDetail";
import LessonReader from "./pages/LessonReader";
import Quiz from "./pages/Quiz";
import Certificates from "./pages/Certificates";
import InstructorDashboard from "./pages/InstructorDashboard";
import InstructorRoster from "./pages/InstructorRoster";
import InstructorCourseEditor from "./pages/InstructorCourseEditor";
import NotFound from "./pages/NotFound";

function AppLayout({ children }) {
  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <div className="flex-1">{children}</div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider>
          <AppLayout>
            <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/onboarding" element={<RequireAuth><Onboarding /></RequireAuth>} />
              <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
              <Route path="/catalog" element={<RequireAuth><Catalog /></RequireAuth>} />
              <Route path="/courses/:courseId" element={<RequireAuth><CourseDetail /></RequireAuth>} />
              <Route path="/courses/:courseId/learn/:lessonId" element={<RequireAuth><LessonReader /></RequireAuth>} />
              <Route path="/courses/:courseId/quiz/:quizId" element={<RequireAuth><Quiz /></RequireAuth>} />
              <Route path="/certificates" element={<RequireAuth><Certificates /></RequireAuth>} />
              <Route path="/instructor" element={<RequireInstructor><InstructorDashboard /></RequireInstructor>} />
              <Route path="/instructor/courses/:courseId" element={<RequireInstructor><InstructorCourseEditor /></RequireInstructor>} />
              <Route path="/instructor/courses/:courseId/roster" element={<RequireInstructor><InstructorRoster /></RequireInstructor>} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </AppLayout>
        </ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
