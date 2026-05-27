import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Резюме
export const getResumes = () => api.get('/resume/resumes-all/');
export const getResume = (id) => api.get(`/resume/resumes-all/${id}/`);
export const createResume = (data) => api.post('/resume/resumes-all/', data);
export const updateResume = (id, data) => api.put(`/resume/resumes-all/${id}/`, data);
export const deleteResume = (id) => api.delete(`/resume/resumes-all/${id}/`);

// Вакансии
export const getVacancies = () => api.get('/resume/vacancies-all/');
export const getVacancy = (id) => api.get(`/resume/vacancies-all/${id}/`);
export const createVacancy = (data) => api.post('/resume/vacancies-all/', data);
export const updateVacancy = (id, data) => api.put(`/resume/vacancies-all/${id}/`, data);
export const deleteVacancy = (id) => api.delete(`/resume/vacancies-all/${id}/`);

// Адаптация
export const adaptResume = (data) => api.post('/resume/adapted-resume/', data);

export default api;