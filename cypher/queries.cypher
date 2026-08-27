
// 1. CONSTRAINTS 

CREATE CONSTRAINT persona_id_unique IF NOT EXISTS
FOR (p:Persona) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT carrera_id_unique IF NOT EXISTS
FOR (c:Carrera) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT habilidad_id_unique IF NOT EXISTS
FOR (h:Habilidad) REQUIRE h.id IS UNIQUE;


// 2. HABILIDADES - Insertadas

MERGE (:Habilidad {id: 'h1',  nombre: 'Pensamiento logico',        categoria: 'Cognitiva'});
MERGE (:Habilidad {id: 'h2',  nombre: 'Programacion',               categoria: 'Tecnica'});
MERGE (:Habilidad {id: 'h3',  nombre: 'Analisis matematico',        categoria: 'Cognitiva'});
MERGE (:Habilidad {id: 'h4',  nombre: 'Creatividad',                categoria: 'Blanda'});
MERGE (:Habilidad {id: 'h5',  nombre: 'Comunicacion oral',          categoria: 'Blanda'});
MERGE (:Habilidad {id: 'h6',  nombre: 'Comunicacion escrita',       categoria: 'Blanda'});
MERGE (:Habilidad {id: 'h7',  nombre: 'Trabajo en equipo',          categoria: 'Blanda'});
MERGE (:Habilidad {id: 'h8',  nombre: 'Empatia',                    categoria: 'Blanda'});
MERGE (:Habilidad {id: 'h9',  nombre: 'Diseno visual',              categoria: 'Tecnica'});
MERGE (:Habilidad {id: 'h10', nombre: 'Resolucion de problemas',    categoria: 'Cognitiva'});
MERGE (:Habilidad {id: 'h11', nombre: 'Investigacion cientifica',   categoria: 'Academica'});
MERGE (:Habilidad {id: 'h12', nombre: 'Liderazgo',                  categoria: 'Blanda'});
MERGE (:Habilidad {id: 'h13', nombre: 'Manejo de datos',            categoria: 'Tecnica'});
MERGE (:Habilidad {id: 'h14', nombre: 'Habilidad manual/tecnica',   categoria: 'Tecnica'});
MERGE (:Habilidad {id: 'h15', nombre: 'Pensamiento critico',        categoria: 'Cognitiva'});


// 3. CARRERAS + relacion REQUIERE

MERGE (c:Carrera {id: 'c1', nombre: 'Ingenieria de Sistemas', descripcion: 'Diseno y desarrollo de software y sistemas de informacion', facultad: 'Ingenieria'})
WITH c
MATCH (h:Habilidad) WHERE h.id IN ['h1','h2','h10','h3']
MERGE (c)-[:REQUIERE]->(h);

MERGE (c:Carrera {id: 'c2', nombre: 'Ingenieria Industrial', descripcion: 'Optimizacion de procesos y recursos productivos', facultad: 'Ingenieria'})
WITH c
MATCH (h:Habilidad) WHERE h.id IN ['h3','h13','h12','h10']
MERGE (c)-[:REQUIERE]->(h);

MERGE (c:Carrera {id: 'c3', nombre: 'Psicologia', descripcion: 'Estudio del comportamiento y procesos mentales', facultad: 'Ciencias Sociales'})
WITH c
MATCH (h:Habilidad) WHERE h.id IN ['h8','h5','h11','h15']
MERGE (c)-[:REQUIERE]->(h);

MERGE (c:Carrera {id: 'c4', nombre: 'Diseno Grafico', descripcion: 'Creacion de piezas visuales y comunicacion grafica', facultad: 'Artes'})
WITH c
MATCH (h:Habilidad) WHERE h.id IN ['h4','h9','h6']
MERGE (c)-[:REQUIERE]->(h);

MERGE (c:Carrera {id: 'c5', nombre: 'Medicina', descripcion: 'Diagnostico, tratamiento y prevencion de enfermedades', facultad: 'Ciencias de la Salud'})
WITH c
MATCH (h:Habilidad) WHERE h.id IN ['h11','h15','h8','h10']
MERGE (c)-[:REQUIERE]->(h);

MERGE (c:Carrera {id: 'c6', nombre: 'Derecho', descripcion: 'Estudio y aplicacion de las normas juridicas', facultad: 'Ciencias Sociales'})
WITH c
MATCH (h:Habilidad) WHERE h.id IN ['h5','h6','h15']
MERGE (c)-[:REQUIERE]->(h);

MERGE (c:Carrera {id: 'c7', nombre: 'Administracion de Empresas', descripcion: 'Gestion de organizaciones y recursos', facultad: 'Ciencias Economicas'})
WITH c
MATCH (h:Habilidad) WHERE h.id IN ['h12','h7','h13']
MERGE (c)-[:REQUIERE]->(h);

MERGE (c:Carrera {id: 'c8', nombre: 'Comunicacion Social', descripcion: 'Produccion y gestion de contenidos y medios', facultad: 'Ciencias Sociales'})
WITH c
MATCH (h:Habilidad) WHERE h.id IN ['h5','h6','h4']
MERGE (c)-[:REQUIERE]->(h);


// 4. PERSONAS + relacion LE_GUSTA

MERGE (p:Persona {id: 'p1', nombre: 'Camila Torres', edad: 17, nivel_educativo: 'Bachillerato', email: 'camila.torres@example.com'})
WITH p
MATCH (h:Habilidad) WHERE h.id IN ['h1','h2','h10','h13']
MERGE (p)-[:LE_GUSTA]->(h);

MERGE (p:Persona {id: 'p2', nombre: 'Daniel Rojas', edad: 18, nivel_educativo: 'Bachillerato', email: 'daniel.rojas@example.com'})
WITH p
MATCH (h:Habilidad) WHERE h.id IN ['h11','h15','h8','h5']
MERGE (p)-[:LE_GUSTA]->(h);

MERGE (p:Persona {id: 'p3', nombre: 'Valentina Perez', edad: 17, nivel_educativo: 'Bachillerato', email: 'valentina.perez@example.com'})
WITH p
MATCH (h:Habilidad) WHERE h.id IN ['h8','h5','h15','h7']
MERGE (p)-[:LE_GUSTA]->(h);

MERGE (p:Persona {id: 'p4', nombre: 'Andres Gomez', edad: 19, nivel_educativo: 'Tecnico', email: 'andres.gomez@example.com'})
WITH p
MATCH (h:Habilidad) WHERE h.id IN ['h5','h6','h15','h12']
MERGE (p)-[:LE_GUSTA]->(h);

MERGE (p:Persona {id: 'p5', nombre: 'Laura Jimenez', edad: 18, nivel_educativo: 'Bachillerato', email: 'laura.jimenez@example.com'})
WITH p
MATCH (h:Habilidad) WHERE h.id IN ['h5','h6','h4','h9']
MERGE (p)-[:LE_GUSTA]->(h);

// 5. VERIFICACION RAPIDA 

MATCH (n) RETURN labels(n) AS tipo, count(n) AS total;

MATCH (p:Persona)-[:LE_GUSTA]->(h:Habilidad) RETURN p.nombre, collect(h.nombre);

MATCH (c:Carrera)-[:REQUIERE]->(h:Habilidad) RETURN c.nombre, collect(h.nombre);
