import streamlit as st
import requests
import os
from typing import List, Dict, Any

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="CareerGraph - Recomendación de Carreras",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4a4a6a;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .compat-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    .compat-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: #667eea;
    }
    .compat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .compat-career {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a2e;
    }
    .compat-score {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
    }
    .compat-details {
        color: #666;
        font-size: 0.9rem;
    }
    .progress-container {
        height: 8px;
        background: #f0f0f0;
        border-radius: 4px;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    .skill-tag {
        display: inline-block;
        background: #f0f0f0;
        color: #333;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    .skill-tag.selected {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a1a2e;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60)
def fetch_personas() -> List[Dict]:
    try:
        resp = requests.get(f"{API_URL}/personas", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error al cargar personas: {e}")
        return []


@st.cache_data(ttl=60)
def fetch_carreras() -> List[Dict]:
    try:
        resp = requests.get(f"{API_URL}/carreras", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error al cargar carreras: {e}")
        return []


@st.cache_data(ttl=60)
def fetch_habilidades() -> List[Dict]:
    try:
        resp = requests.get(f"{API_URL}/habilidades", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error al cargar habilidades: {e}")
        return []


def fetch_compatibilidad(persona_id: str) -> List[Dict]:
    try:
        resp = requests.get(f"{API_URL}/compatibilidad/{persona_id}", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error al calcular compatibilidad: {e}")
        return []


def fetch_stats() -> Dict:
    try:
        resp = requests.get(f"{API_URL}/stats", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {"total_personas": 0, "total_carreras": 0, "total_habilidades": 0}


def render_header():
    st.markdown('<div class="main-header">🎓 CareerGraph</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sistema de recomendación de carreras basado en grafos — Neo4j + Python</div>', unsafe_allow_html=True)


def render_stats():
    stats = fetch_stats()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{stats.get("total_personas", 0)}</div>
                <div class="metric-label">Personas</div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{stats.get("total_carreras", 0)}</div>
                <div class="metric-label">Carreras</div>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{stats.get("total_habilidades", 0)}</div>
                <div class="metric-label">Habilidades</div>
            </div>
        ''', unsafe_allow_html=True)


def render_persona_selector(personas: List[Dict]):
    st.markdown('<div class="section-title">👤 Seleccionar Persona</div>', unsafe_allow_html=True)
    
    if not personas:
        st.warning("No hay personas registradas. Agrega una desde la pestaña 'Administración'.")
        return None
    
    options = {f"{p['nombre']} ({p['email']})": p['id'] for p in personas}
    selected_label = st.selectbox(
        "Elige una persona para ver sus recomendaciones:",
        options=list(options.keys()),
        index=0,
        label_visibility="collapsed"
    )
    return options[selected_label]


def render_persona_skills(persona_id: str, personas: List[Dict], all_habilidades: List[Dict]):
    persona = next((p for p in personas if p['id'] == persona_id), None)
    if not persona:
        return
    
    habilidades_map = {h['id']: h for h in all_habilidades}
    persona_skills = persona.get('habilidades', [])
    
    st.markdown('<div class="section-title">🎯 Habilidades de la Persona</div>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, skill_id in enumerate(persona_skills):
        skill = habilidades_map.get(skill_id)
        if skill:
            with cols[i % 4]:
                st.markdown(f'''
                    <span class="skill-tag selected">
                        {skill['nombre']} <small>({skill['categoria']})</small>
                    </span>
                ''', unsafe_allow_html=True)


def render_compatibilidad(results: List[Dict]):
    st.markdown('<div class="section-title">📊 Resultados de Compatibilidad</div>', unsafe_allow_html=True)
    
    if not results:
        st.info("No se encontraron resultados de compatibilidad.")
        return
    
    for r in results:
        compat = r['compatibilidad']
        color = "#22c55e" if compat >= 70 else "#f59e0b" if compat >= 40 else "#ef4444"
        
        st.markdown(f'''
            <div class="compat-card">
                <div class="compat-header">
                    <span class="compat-career">{r['carrera']}</span>
                    <span class="compat-score" style="color: {color};">{compat}%</span>
                </div>
                <div class="compat-details">
                    {r['coincidencias']} de {r['total_requeridas']} habilidades coinciden
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {compat}%;"></div>
                </div>
            </div>
        ''', unsafe_allow_html=True)


def render_admin_tab():
    st.markdown('<div class="section-title">⚙️ Administración</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["➕ Nueva Persona", "➕ Nueva Carrera", "➕ Nueva Habilidad"])
    
    with tab1:
        with st.form("nueva_persona"):
            st.subheader("Crear Persona")
            nombre = st.text_input("Nombre completo")
            email = st.text_input("Email")
            edad = st.number_input("Edad", min_value=14, max_value=100, value=18)
            nivel = st.selectbox("Nivel educativo", ["Bachillerato", "Tecnico", "Universitario", "Postgrado"])
            
            habilidades = fetch_habilidades()
            habilidades_seleccionadas = st.multiselect(
                "Habilidades / Intereses",
                options=[h['id'] for h in habilidades],
                format_func=lambda x: next((h['nombre'] for h in habilidades if h['id'] == x), x)
            )
            
            if st.form_submit_button("Crear Persona"):
                if nombre and email:
                    try:
                        resp = requests.post(
                            f"{API_URL}/personas",
                            json={
                                "nombre": nombre,
                                "email": email,
                                "edad": edad,
                                "nivel_educativo": nivel,
                                "habilidades_ids": habilidades_seleccionadas
                            },
                            timeout=10
                        )
                        if resp.status_code == 201:
                            st.success("Persona creada correctamente!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Error: {resp.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Completa todos los campos obligatorios")
    
    with tab2:
        with st.form("nueva_carrera"):
            st.subheader("Crear Carrera")
            nombre = st.text_input("Nombre de la carrera")
            descripcion = st.text_area("Descripción")
            facultad = st.text_input("Facultad")
            
            habilidades = fetch_habilidades()
            requiere = st.multiselect(
                "Habilidades requeridas",
                options=[h['id'] for h in habilidades],
                format_func=lambda x: next((h['nombre'] for h in habilidades if h['id'] == x), x)
            )
            
            if st.form_submit_button("Crear Carrera"):
                if nombre and descripcion and facultad:
                    try:
                        resp = requests.post(
                            f"{API_URL}/carreras",
                            json={
                                "nombre": nombre,
                                "descripcion": descripcion,
                                "facultad": facultad,
                                "requiere": requiere
                            },
                            timeout=10
                        )
                        if resp.status_code == 201:
                            st.success("Carrera creada correctamente!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Error: {resp.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Completa todos los campos obligatorios")
    
    with tab3:
        with st.form("nueva_habilidad"):
            st.subheader("Crear Habilidad")
            nombre = st.text_input("Nombre de la habilidad")
            categoria = st.selectbox("Categoría", ["Cognitiva", "Tecnica", "Blanda", "Academica"])
            
            if st.form_submit_button("Crear Habilidad"):
                if nombre:
                    try:
                        resp = requests.post(
                            f"{API_URL}/habilidades",
                            json={"nombre": nombre, "categoria": categoria},
                            timeout=10
                        )
                        if resp.status_code == 201:
                            st.success("Habilidad creada correctamente!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Error: {resp.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Completa el nombre")


def main():
    render_header()
    render_stats()
    
    personas = fetch_personas()
    carreras = fetch_carreras()
    habilidades = fetch_habilidades()
    
    tab_recomendaciones, tab_admin = st.tabs(["🎯 Recomendaciones", "⚙️ Administración"])
    
    with tab_recomendaciones:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            persona_id = render_persona_selector(personas)
            if persona_id:
                render_persona_skills(persona_id, personas, habilidades)
        
        with col2:
            if persona_id:
                with st.spinner("Calculando compatibilidad..."):
                    results = fetch_compatibilidad(persona_id)
                render_compatibilidad(results)
            else:
                st.info("Selecciona una persona para ver las recomendaciones")
    
    with tab_admin:
        render_admin_tab()
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; font-size: 0.85rem;'>"
        "CareerGraph — Proyecto de Bases de Datos No Relacionales • Neo4j + FastAPI + Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()