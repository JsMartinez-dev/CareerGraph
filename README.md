# CareerGraph 

Sistema de recomendación de carreras basado en grafos, construido con **Neo4j** y **Python**. A partir de los intereses y habilidades de una persona, calcula un porcentaje de compatibilidad con distintas carreras universitarias.

Proyecto desarrollado para la clase de base de datos no relacionales — 27/08/2026.

---

##  Autores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/JsMartinez-dev">
        <img src="https://github.com/JsMartinez-dev.png" width="100px;" alt="Juan Sebastian Martinez Uribe"/>
        <br />
        <b>Juan Sebastian Martinez Uribe</b>
      </a>
      <br />
      Modelado de datos y queries Cypher
    </td>
    <td align="center">
      <a href="https://github.com/ginozza">
        <img src="https://github.com/ginozza.png" width="100px;" alt="Juan Manuel Simancas Martinez"/>
        <br />
        <b>Juan Manuel Simancas Martinez</b>
      </a>
      <br />
      Backend Python y conexión a base de datos
    </td>
  </tr>
</table>


---

##  Descripción del problema

Elegir una carrera universitaria es una decisión difícil cuando no se tiene claridad sobre qué opciones se alinean con los intereses y habilidades propias. **CareerGraph** resuelve esto modelando personas, carreras y habilidades como un grafo, permitiendo calcular qué tan compatible es una persona con cada carrera disponible según las conexiones que comparten.

---

##  Modelo de datos

**Nodos:**
- `Persona` — usuario del sistema
- `Carrera` — carrera universitaria disponible
- `Habilidad` — habilidad o interés específico

**Relaciones:**
- `(Persona)-[:LE_GUSTA]->(Habilidad)`
- `(Carrera)-[:REQUIERE]->(Habilidad)`

**Cálculo de compatibilidad:**


Se utiliza la siguiente fórmula:

$$
Compatibilidad =
\frac{\text{Habilidades coincidentes}}
{\text{Total de habilidades requeridas}}
\times 100
$$

Donde:

- Habilidades coincidentes: habilidades que la persona tiene en común con las requeridas por la carrera.
- Total de habilidades requeridas: cantidad total de habilidades que requiere la carrera.
- Compatibilidad: porcentaje de coincidencia entre la persona y la carrera.
---

##  Tecnologías

- [Neo4j](https://neo4j.com/) (AuraDB) — base de datos de grafos
- [Python 3.x](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) — API backend
- [Streamlit](https://streamlit.io/) — interfaz web
- [neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [Pydantic](https://docs.pydantic.dev/) — validación de datos

---

## 📁 Estructura del proyecto

```
careergraph/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── cypher/
│   └── queries.cypher           # Queries de consulta y recomendación
├── database/
│   ├── conexion.py              # Conexión al driver de Neo4j (legacy)
│   └── crud.py                  # Funciones de insert / update / query (legacy)
├── backend/                     # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                  # Aplicación FastAPI
│   ├── config.py                # Configuración y settings
│   ├── database.py              # Conexión a Neo4j
│   ├── models.py                # Modelos Pydantic
│   └── crud.py                  # Operaciones CRUD
├── frontend/                    # Streamlit Frontend
│   └── app.py                   # Aplicación Streamlit
└── data/
    └── carga_inicial.py         # Script de carga de datos de ejemplo
```

---

##  Instalación y ejecución

1. Clonar el repositorio
   ```bash
   git clone https://github.com/[usuario]/careergraph.git
   cd careergraph
   ```

2. Crear entorno virtual e instalar dependencias
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar credenciales
   - Copiar `.env.example` a `.env`
   - Completar con las credenciales de tu instancia de Neo4j AuraDB (URI, usuario, contraseña)

4. Cargar datos iniciales
   ```bash
   python data/carga_inicial.py
   ```

5. Ejecutar el backend (API)
   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

6. Ejecutar el frontend (en otra terminal)
   ```bash
   streamlit run frontend/app.py
   ```

---

##  API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check (verifica BD) |
| GET | `/stats` | Estadísticas de la BD |
| GET | `/personas` | Listar personas |
| GET | `/personas/{id}` | Obtener persona |
| POST | `/personas` | Crear persona |
| PUT | `/personas/{id}` | Actualizar persona |
| DELETE | `/personas/{id}` | Eliminar persona |
| GET | `/carreras` | Listar carreras |
| GET | `/carreras/{id}` | Obtener carrera |
| POST | `/carreras` | Crear carrera |
| GET | `/habilidades` | Listar habilidades |
| GET | `/habilidades/{id}` | Obtener habilidad |
| POST | `/habilidades` | Crear habilidad |
| GET | `/compatibilidad/{persona_id}` | Calcular compatibilidad |

---

##  Funcionalidades

- [x] Modelado de personas, carreras y habilidades como grafo
- [x] Inserción y actualización de datos vía Python (CRUD)
- [x] Consulta de compatibilidad persona–carrera
- [x] API REST completa con FastAPI
- [x] Interfaz web moderna con Streamlit
- [x] Administración de personas, carreras y habilidades desde la UI

---

##  Demo

![Grafo en Neo4j Browser](imgs/nodos_realaciones.png)

![Tabla de compatibilidad](imgs/tabla_compatibilidad.png)
---

##  Licencia

MIT