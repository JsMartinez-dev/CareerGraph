import { useState, useEffect, useMemo } from 'react';
import apiService from './api';
import type { Persona, Habilidad, Compatibilidad, Stats, CreatePersona, CreateCarrera, CreateHabilidad } from './types';
import './App.css';

function App() {
  // State
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [habilidades, setHabilidades] = useState<Habilidad[]>([]);
  const [compatibilidad, setCompatibilidad] = useState<Compatibilidad[]>([]);
  const [stats, setStats] = useState<Stats>({ total_personas: 0, total_carreras: 0, total_habilidades: 0 });
  const [selectedPersonaId, setSelectedPersonaId] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'recomendaciones' | 'admin'>('recomendaciones');
  const [adminTab, setAdminTab] = useState<'persona' | 'carrera' | 'habilidad'>('persona');
  const [error, setError] = useState<string | null>(null);

  // Forms state
  const [personaForm, setPersonaForm] = useState<CreatePersona>({
    nombre: '', email: '', edad: 18, nivel_educativo: 'Bachillerato', habilidades_ids: []
  });
  const [carreraForm, setCarreraForm] = useState<CreateCarrera>({
    nombre: '', descripcion: '', facultad: '', requiere: []
  });
  const [habilidadForm, setHabilidadForm] = useState<CreateHabilidad>({
    nombre: '', categoria: 'Cognitiva'
  });

  // Load initial data
  const loadData = async () => {
    setLoading(true);
    try {
      const [p, h, s] = await Promise.all([
        apiService.getPersonas(),
        apiService.getHabilidades(),
        apiService.stats(),
      ]);
      setPersonas(p.data);
      setHabilidades(h.data);
      setStats(s.data);
      
      if (p.data.length > 0 && !selectedPersonaId) {
        setSelectedPersonaId(p.data[0].id);
      }
    } catch (err) {
      setError('Error cargando datos: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  // Load compatibilidad when persona changes
  useEffect(() => {
    if (selectedPersonaId) {
      apiService.getCompatibilidad(selectedPersonaId)
        .then(res => setCompatibilidad(res.data))
        .catch(err => setError('Error calculando compatibilidad: ' + err.message));
    } else {
      setCompatibilidad([]);
    }
  }, [selectedPersonaId]);

  useEffect(() => {
    loadData();
  }, []);

  // Form handlers
  const handlePersonaSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiService.createPersona(personaForm);
      await loadData();
      setPersonaForm({ nombre: '', email: '', edad: 18, nivel_educativo: 'Bachillerato', habilidades_ids: [] });
    } catch (err) {
      setError('Error creando persona: ' + (err as Error).message);
    }
  };

  const handleCarreraSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiService.createCarrera(carreraForm);
      await loadData();
      setCarreraForm({ nombre: '', descripcion: '', facultad: '', requiere: [] });
    } catch (err) {
      setError('Error creando carrera: ' + (err as Error).message);
    }
  };

  const handleHabilidadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiService.createHabilidad(habilidadForm);
      await loadData();
      setHabilidadForm({ nombre: '', categoria: 'Cognitiva' });
    } catch (err) {
      setError('Error creando habilidad: ' + (err as Error).message);
    }
  };

  // Computed
  const selectedPersona = useMemo(() => 
    personas.find(p => p.id === selectedPersonaId), 
    [personas, selectedPersonaId]
  );

  const categorias = ['Cognitiva', 'Tecnica', 'Blanda', 'Academica'] as const;
  type Categoria = typeof categorias[number];
  const habilidadesByCategoria = useMemo(() => {
    const grouped: Record<Categoria, Habilidad[]> = {
      Cognitiva: [], Tecnica: [], Blanda: [], Academica: []
    };
    habilidades.forEach(h => {
      if (categorias.includes(h.categoria as Categoria)) {
        grouped[h.categoria as Categoria].push(h);
      }
    });
    return grouped;
  }, [habilidades]);

  const getCompatColor = (pct: number) => 
    pct >= 70 ? '#22c55e' : pct >= 40 ? '#f59e0b' : '#ef4444';

  if (loading && personas.length === 0) {
    return <div className="loading">Cargando...</div>;
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>CareerGraph</h1>
          <p>Recomendación de carreras basada en grafos — Neo4j + FastAPI + React</p>
        </div>
        <div className="stats-bar">
          <div className="stat"><span>{stats.total_personas}</span> Personas</div>
          <div className="stat"><span>{stats.total_carreras}</span> Carreras</div>
          <div className="stat"><span>{stats.total_habilidades}</span> Habilidades</div>
        </div>
      </header>

      {error && <div className="error-banner" onClick={() => setError(null)}>{error} ×</div>}

      <nav className="tabs">
        <button className={activeTab === 'recomendaciones' ? 'active' : ''} onClick={() => setActiveTab('recomendaciones')}>
          Recomendaciones
        </button>
        <button className={activeTab === 'admin' ? 'active' : ''} onClick={() => setActiveTab('admin')}>
          Administracion
        </button>
      </nav>

      <main className="main">
        {activeTab === 'recomendaciones' && (
          <div className="recommendations">
            <section className="persona-selector">
              <h2>Seleccionar Persona</h2>
              <select 
                value={selectedPersonaId} 
                onChange={e => setSelectedPersonaId(e.target.value)}
                disabled={personas.length === 0}
              >
                {personas.map(p => (
                  <option key={p.id} value={p.id}>
                    {p.nombre} ({p.email})
                  </option>
                ))}
              </select>
            </section>

            {selectedPersona && (
              <section className="persona-skills">
                <h2>Habilidades de {selectedPersona.nombre}</h2>
                <div className="skills-grid">
                  {categorias.map(cat => (
                    <div key={cat} className="skill-category">
                      <h4>{cat}</h4>
                      {habilidadesByCategoria[cat].map(h => (
                        <span 
                          key={h.id} 
                          className={`skill-tag ${selectedPersona.habilidades.includes(h.id) ? 'selected' : ''}`}
                        >
                          {h.nombre}
                        </span>
                      ))}
                    </div>
                  ))}
                </div>
              </section>
            )}

            <section className="results">
              <h2>Resultados de Compatibilidad</h2>
              {compatibilidad.length === 0 ? (
                <p className="empty">Selecciona una persona para ver recomendaciones</p>
              ) : (
                <div className="results-grid">
                  {compatibilidad.map((r, i) => (
                    <div key={i} className="result-card">
                      <div className="result-header">
                        <span className="career-name">{r.carrera}</span>
                        <span className="score" style={{ color: getCompatColor(r.compatibilidad) }}>
                          {r.compatibilidad}%
                        </span>
                      </div>
                      <div className="details">
                        {r.coincidencias} de {r.total_requeridas} habilidades coinciden
                      </div>
                      <div className="progress-bar">
                        <div 
                          className="progress-fill" 
                          style={{ width: `${r.compatibilidad}%`, background: getCompatColor(r.compatibilidad) }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        )}

        {activeTab === 'admin' && (
          <div className="admin">
            <nav className="admin-tabs">
              <button className={adminTab === 'persona' ? 'active' : ''} onClick={() => setAdminTab('persona')}>Persona</button>
              <button className={adminTab === 'carrera' ? 'active' : ''} onClick={() => setAdminTab('carrera')}>Carrera</button>
              <button className={adminTab === 'habilidad' ? 'active' : ''} onClick={() => setAdminTab('habilidad')}>Habilidad</button>
            </nav>

            {adminTab === 'persona' && (
              <form onSubmit={handlePersonaSubmit} className="admin-form">
                <h3>Nueva Persona</h3>
                <div className="form-row">
                  <input 
                    placeholder="Nombre completo" 
                    value={personaForm.nombre} 
                    onChange={e => setPersonaForm({...personaForm, nombre: e.target.value})} 
                    required 
                  />
                  <input 
                    type="email" 
                    placeholder="Email" 
                    value={personaForm.email} 
                    onChange={e => setPersonaForm({...personaForm, email: e.target.value})} 
                    required 
                  />
                </div>
                <div className="form-row">
                  <input 
                    type="number" 
                    placeholder="Edad" 
                    min="14" max="100"
                    value={personaForm.edad} 
                    onChange={e => setPersonaForm({...personaForm, edad: parseInt(e.target.value)})} 
                    required 
                  />
                  <select 
                    value={personaForm.nivel_educativo} 
                    onChange={e => setPersonaForm({...personaForm, nivel_educativo: e.target.value})}
                  >
                    <option value="Bachillerato">Bachillerato</option>
                    <option value="Tecnico">Técnico</option>
                    <option value="Universitario">Universitario</option>
                    <option value="Postgrado">Postgrado</option>
                  </select>
                </div>
                <div className="form-field">
                  <label>Habilidades / Intereses</label>
                  <div className="checkbox-grid">
                    {habilidades.map(h => (
                      <label key={h.id} className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={personaForm.habilidades_ids.includes(h.id)}
                          onChange={e => setPersonaForm({
                            ...personaForm,
                            habilidades_ids: e.target.checked
                              ? [...personaForm.habilidades_ids, h.id]
                              : personaForm.habilidades_ids.filter(id => id !== h.id)
                          })}
                        />
                        {h.nombre} <small>({h.categoria})</small>
                      </label>
                    ))}
                  </div>
                </div>
                <button type="submit" className="btn-primary">Crear Persona</button>
              </form>
            )}

            {adminTab === 'carrera' && (
              <form onSubmit={handleCarreraSubmit} className="admin-form">
                <h3>Nueva Carrera</h3>
                <input 
                  placeholder="Nombre de la carrera" 
                  value={carreraForm.nombre} 
                  onChange={e => setCarreraForm({...carreraForm, nombre: e.target.value})} 
                  required 
                />
                <textarea 
                  placeholder="Descripción" 
                  value={carreraForm.descripcion} 
                  onChange={e => setCarreraForm({...carreraForm, descripcion: e.target.value})} 
                  required 
                />
                <input 
                  placeholder="Facultad" 
                  value={carreraForm.facultad} 
                  onChange={e => setCarreraForm({...carreraForm, facultad: e.target.value})} 
                  required 
                />
                <div className="form-field">
                  <label>Habilidades requeridas</label>
                  <div className="checkbox-grid">
                    {habilidades.map(h => (
                      <label key={h.id} className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={carreraForm.requiere.includes(h.id)}
                          onChange={e => setCarreraForm({
                            ...carreraForm,
                            requiere: e.target.checked
                              ? [...carreraForm.requiere, h.id]
                              : carreraForm.requiere.filter(id => id !== h.id)
                          })}
                        />
                        {h.nombre} <small>({h.categoria})</small>
                      </label>
                    ))}
                  </div>
                </div>
                <button type="submit" className="btn-primary">Crear Carrera</button>
              </form>
            )}

            {adminTab === 'habilidad' && (
              <form onSubmit={handleHabilidadSubmit} className="admin-form">
                <h3>Nueva Habilidad</h3>
                <input 
                  placeholder="Nombre de la habilidad" 
                  value={habilidadForm.nombre} 
                  onChange={e => setHabilidadForm({...habilidadForm, nombre: e.target.value})} 
                  required 
                />
                <select 
                  value={habilidadForm.categoria} 
                  onChange={e => setHabilidadForm({...habilidadForm, categoria: e.target.value})}
                >
                  <option value="Cognitiva">Cognitiva</option>
                  <option value="Tecnica">Técnica</option>
                  <option value="Blanda">Blanda</option>
                  <option value="Academica">Académica</option>
                </select>
                <button type="submit" className="btn-primary">Crear Habilidad</button>
              </form>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        CareerGraph — Neo4j + FastAPI + React TypeScript
      </footer>
    </div>
  );
}

export default App;