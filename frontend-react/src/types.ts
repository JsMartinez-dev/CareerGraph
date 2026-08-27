export interface Persona {
  id: string;
  nombre: string;
  edad: number;
  nivel_educativo: string;
  email: string;
  habilidades: string[];
}

export interface Carrera {
  id: string;
  nombre: string;
  descripcion: string;
  facultad: string;
  requiere: string[];
}

export interface Habilidad {
  id: string;
  nombre: string;
  categoria: string;
}

export interface Compatibilidad {
  carrera: string;
  coincidencias: number;
  total_requeridas: number;
  compatibilidad: number;
}

export interface Stats {
  total_personas: number;
  total_carreras: number;
  total_habilidades: number;
}

export interface CreatePersona {
  nombre: string;
  email: string;
  edad: number;
  nivel_educativo: string;
  habilidades_ids: string[];
}

export interface CreateCarrera {
  nombre: string;
  descripcion: string;
  facultad: string;
  requiere: string[];
}

export interface CreateHabilidad {
  nombre: string;
  categoria: string;
}