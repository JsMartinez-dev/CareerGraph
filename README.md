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
- [Streamlit](https://streamlit.io/) — interfaz web
- [neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)

---

## 📁 Estructura del proyecto

```
careergraph/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── cypher/
│   └── queries.cypher       # Queries de consulta y recomendación
├── database/
│   ├── conexion.py          # Conexión al driver de Neo4j
│   └── crud.py              # Funciones de insert / update / query
├── app/
│   └── main.py               # Aplicación Streamlit
└── data/
    └── carga_inicial.py      # Script de carga de datos de ejemplo
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

5. Ejecutar la aplicación
   ```bash
   streamlit run app/main.py
   ```

---

##  Funcionalidades

- [x] Modelado de personas, carreras y habilidades como grafo
- [x] Inserción y actualización de datos vía Python (CRUD)
- [x] Consulta de compatibilidad persona–carrera
- [x] Interfaz web simple para seleccionar intereses y ver resultados

---

##  Demo

*(Agregar aquí capturas de pantalla o GIF de la app funcionando antes de la entrega)*

---

##  Licencia

Proyecto académico, uso educativo.
