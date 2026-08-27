import axios from 'axios';
import type { Persona, Carrera, Habilidad, Compatibilidad, Stats, CreatePersona, CreateCarrera, CreateHabilidad } from './types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

export const apiService = {
  // Health & Stats
  health: () => api.get('/health'),
  stats: () => api.get<Stats>('/stats'),

  // Personas
  getPersonas: () => api.get<Persona[]>('/personas'),
  getPersona: (id: string) => api.get<Persona>(`/personas/${id}`),
  createPersona: (data: CreatePersona) => api.post<Persona>('/personas', data),
  updatePersona: (id: string, data: CreatePersona) => api.put<Persona>(`/personas/${id}`, data),
  deletePersona: (id: string) => api.delete(`/personas/${id}`),

  // Carreras
  getCarreras: () => api.get<Carrera[]>('/carreras'),
  getCarrera: (id: string) => api.get<Carrera>(`/carreras/${id}`),
  createCarrera: (data: CreateCarrera) => api.post<Carrera>('/carreras', data),

  // Habilidades
  getHabilidades: () => api.get<Habilidad[]>('/habilidades'),
  getHabilidad: (id: string) => api.get<Habilidad>(`/habilidades/${id}`),
  createHabilidad: (data: CreateHabilidad) => api.post<Habilidad>('/habilidades', data),

  // Compatibilidad
  getCompatibilidad: (personaId: string) => api.get<Compatibilidad[]>(`/compatibilidad/${personaId}`),
};

export default apiService;