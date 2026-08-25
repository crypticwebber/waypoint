import api from "./client";

export const authApi = {
  register: (payload) => api.post("/auth/register", payload).then((r) => r.data),
  login: (payload) => api.post("/auth/login", payload).then((r) => r.data),
  me: () => api.get("/auth/me").then((r) => r.data),
};

export const preferencesApi = {
  get: () => api.get("/preferences/me").then((r) => r.data),
  save: (payload) => api.put("/preferences/me", payload).then((r) => r.data),
};

export const coursesApi = {
  list: (params) => api.get("/courses", { params }).then((r) => r.data),
  categories: () => api.get("/courses/categories").then((r) => r.data),
  get: (id) => api.get(`/courses/${id}`).then((r) => r.data),
};

export const learningApi = {
  enroll: (courseId) => api.post(`/courses/${courseId}/enroll`).then((r) => r.data),
  completeLesson: (lessonId) => api.post(`/lessons/${lessonId}/complete`).then((r) => r.data),
  submitQuiz: (quizId, answers) => api.post(`/quizzes/${quizId}/attempts`, { answers }).then((r) => r.data),
  quizHistory: (quizId) => api.get(`/quizzes/${quizId}/attempts`).then((r) => r.data),
};

export const reviewsApi = {
  list: (courseId) => api.get(`/courses/${courseId}/reviews`).then((r) => r.data),
  create: (courseId, payload) => api.post(`/courses/${courseId}/reviews`, payload).then((r) => r.data),
};

export const certificatesApi = {
  mine: () => api.get("/certificates/me").then((r) => r.data),
  // The endpoint requires the auth header, so we fetch as a blob (rather than
  // a plain <a href>, which can't attach Authorization) and trigger a download.
  downloadPdf: async (certId, filename) => {
    const response = await api.get(`/certificates/${certId}/pdf`, { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = filename || `waypoint-certificate-${certId}.pdf`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },
};

export const recommendationsApi = {
  mine: (limit = 8) => api.get("/recommendations/me", { params: { limit } }).then((r) => r.data),
};

export const dashboardApi = {
  stats: () => api.get("/dashboard/stats").then((r) => r.data),
  continueLearning: () => api.get("/dashboard/continue-learning").then((r) => r.data),
  completed: () => api.get("/dashboard/completed").then((r) => r.data),
};

export const instructorApi = {
  myCourses: () => api.get("/instructor/courses").then((r) => r.data),
  roster: (courseId) => api.get(`/instructor/courses/${courseId}/roster`).then((r) => r.data),
  createCourse: (payload) => api.post("/instructor/courses", payload).then((r) => r.data),
  updateCourse: (courseId, payload) => api.put(`/instructor/courses/${courseId}`, payload).then((r) => r.data),
  deleteCourse: (courseId) => api.delete(`/instructor/courses/${courseId}`),
  createModule: (courseId, payload) => api.post(`/instructor/courses/${courseId}/modules`, payload).then((r) => r.data),
  updateModule: (moduleId, payload) => api.put(`/instructor/modules/${moduleId}`, payload).then((r) => r.data),
  deleteModule: (moduleId) => api.delete(`/instructor/modules/${moduleId}`),
  createLesson: (moduleId, payload) => api.post(`/instructor/modules/${moduleId}/lessons`, payload).then((r) => r.data),
  updateLesson: (lessonId, payload) => api.put(`/instructor/lessons/${lessonId}`, payload).then((r) => r.data),
  deleteLesson: (lessonId) => api.delete(`/instructor/lessons/${lessonId}`),
  createQuiz: (moduleId, title) => api.post(`/instructor/modules/${moduleId}/quiz`, null, { params: { title } }).then((r) => r.data),
  addQuestion: (quizId, payload) => api.post(`/instructor/quizzes/${quizId}/questions`, payload).then((r) => r.data),
  deleteQuestion: (questionId) => api.delete(`/instructor/questions/${questionId}`),
};
