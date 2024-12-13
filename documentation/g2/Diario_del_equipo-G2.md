# Jamón-Hub - Diario del Equipo

- **Grupo**: G3
- **Nombre del grupo**: jamon-hub-2
- **Tutor**: Jesús Moreno León
- **Curso Escolar**: 2024/2025  
- **Asignatura**: Evolución y Gestión de la Configuración

### Enlaces de interés:

- **Repositorio de código**: [https://github.com/davidgonmar/uvlhub-egc](https://github.com/davidgonmar/uvlhub-egc)  
- **Sistema desplegado**: [https://uvlhub-egc.onrender.com/](https://uvlhub-egc.onrender.com/)

## Índice

1. [Miembros del grupo](#1-miembros-del-grupo)
2. [Resumen de total de reuniones empleadas en el equipo](#2-resumen-de-total-de-reuniones-empleadas-en-el-equipo)
3. [Actas de acuerdos](#3-actas-de-acuerdos)
   - [ACTA 2024-01](#acta-2024-01)
   - [ACTA 2024-02](#acta-2024-02)
   - [ACTA 2024-03](#acta-2024-03)
   - [ACTA 2024-04](#acta-2024-04)
   - [ACTA 2024-05](#acta-2024-05)

---

## 1. Miembros del grupo

| **Nombre Completo**                | **UVUS** | **Email**                       |
|------------------------------------|----------|---------------------------------|
|Barrera Garrancho, María del Carmen | marbargar8  | marbargar8@alum.us.es      |
| García Martínez, Carlos            |cargarmar18| cargarmar18@alum.us.es          |
| García Sebastián, Javier           | javgarseb  | javgarseb@alum.us.es        |
| Meana Iturri, Claudia              | clameaitu| clameaitu@alum.us.es       |
| Pérez Gutiérrez, Lucía             | lucpergut| lucpergut@alum.us.es      |
| Vento Conesa, Adriana              | adrvencon| adrvencon@alum.us.es     |

---

## 2. Resumen de total de reuniones empleadas en el equipo

- **Total de reuniones (TR):** 4
- **Total de reuniones presenciales (TRP):** 1
- **Total de reuniones virtuales (TRV):** 3
- **Total de tiempo empleado en reuniones presenciales (TTRP):** 1h 30min
- **Total de tiempo empleado en reuniones virtuales (TTRV):** 3h

---

## 3. Actas de acuerdos

### ACTA 2024-01

**Asistentes:**

- Barrera Garrancho, María del Carmen
- García Martínez, Carlos
- García Sebastián, Javier
- Meana Iturri, Claudia
- Pérez Gutiérrez, Lucía
- Vento Conesa, Adriana

**Introducción:**

En esta reunión previa al M1, se definieron los Work Items (WIs) a realizar. Dado que se llevó a cabo después de la reunión de **jamon-hub-1**, ya contábamos con información sobre los Work Items seleccionados por ellos, lo que nos permitió ajustar nuestras decisiones. Además, se debatió el uso y la implementación de las políticas a aplicar en el proyecto.

**Acuerdos tomados:**
- **Acuerdo 2024-01-01: Política de Commits**.
Se usará Conventional Commits. Se ha acordado el uso de un Hook para asegurar que todos los commits cumplen la política.

- **Acuerdo 2024-01-02: Estrategia de Ramas**.
Se ha acordado seguir una política de rama por tarea. Los detalles de la estrategia pueden consultarse en el acta fundacional.

- **Acuerdo 2024-01-03: Versionado**.
Se usará Semantic Versioning.

- **Acuerdo 2024-01-04: Work Items**.
Se han discutido los WI a implementar en el proyecto. Se ha acordado, a falta de validación por el profesor, los siguientes WI:  
    - **HIGH**:
        - **Staging Area**: Implementación de un espacio temporal que permite a los usuarios almacenar datasets antes de ser subidos a Zenodo.  
        - **Search Queries**: Desarrollo de funcionalidades avanzadas que permiten a los usuarios realizar consultas específicas para filtrar y descargar modelos según criterios personalizados.
    - **MEDIUM**:
        - **Improve UI**: Rediseño y optimización de la interfaz gráfica de usuario para mejorar la experiencia del usuario. La visualización de los datasets debe ser similar a la de GitHub (como sugerencia).
        - **Different versions of models**: Soporte para diferentes versiones de modelos y su descarga en varios formatos.
    - **LOW**:
        - **Remember my password**: Integración de una funcionalidad que permite a los usuarios optar por guardar su contraseña, facilitando el acceso a la aplicación sin la necesidad de ingresarla repetidamente.
        - **Register developer**: Opción para que los usuarios se registren como desarrolladores.

- **Acuerdo 2024-01-05: Sanciones**:
Se tomaron decisiones que priorizan la comunicación y el apoyo antes de recurrir a medidas más estrictas. Para los casos de bajo rendimiento, se realizarán charlas individuales para entender las preocupaciones de los miembros, reservando la privación de voto como último recurso. En situaciones de ausencias injustificadas en hitos, se documentarán los casos y se evaluará la posible baja del miembro afectado. Respecto a la falta de participación en reuniones, se enviarán recordatorios y se mantendrá una conversación privada si la situación persiste. Se buscarán soluciones a los desacuerdos mediante discusiones abiertas y, de ser necesario, la intervención del coordinador. Por último, se fomentará la capacitación y mentoría entre miembros para mitigar las diferencias de habilidades, y se llevará un registro de conflictos menores, con reuniones periódicas de seguimiento.

- **Acuerdo 2024-01-06: Política de Issues y Gestión de Work Items (WIs)**.
Se decidió que al inicio de cada sprint el equipo descompondrá los Work Items (WIs) en actividades específicas. Las issues se clasificarán en tareas, QA, revisiones e incidencias, cada una asignada a un miembro responsable, con la posibilidad de crear issues adicionales si se requiere colaboración. Las issues seguirán una prioridad (P0 para revisiones, P1 para tareas, P2 para QA) y pasarán por diferentes estados (TODO, In Progress, Pending Review, Failed QA y Done) hasta su conclusión. Se aplicará una nomenclatura estándar para mantener el orden y las etiquetas para clasificar actividades, tipos de cambio y áreas del sistema. Las incidencias se reportarán utilizando una plantilla estandarizada.

### ACTA 2024-02

**Asistentes:**
- Castillo Cebolla, Rafael
- Vento Conesa, Adriana

**Introducción:**
Esta reunión trata los acuerdos tomados entre los coordinadores de ambos grupos de jamon-hub de cara a la segunda _milestone_. 

**Acuerdos tomados:**
- **Acuerdo 2024-02-01:** Definir las tareas a realizar en la segunda iteración, con el fin de anticipar y gestionar los posibles conflictos que puedan surgir.
- **Acuerdo 2024-02-02:** Eliminación de los _issues_ de QA, los cuales serán reemplazados por las revisiones de las _pull requests_, ya que estas cumplen una función equivalente.
- **Acuerdo 2024-02-03:** Eliminación de los _issues_ de revisión. A partir de ahora, se utilizarán las tareas originales para este propósito.
- **Acuerdo 2024-02-04:** Comenzar el estudio del WI 'Fakenodo', aunque no se garantiza que se pueda completar para la _milestone_ 2.
- **Acuerdo 2024-02-05:** Eliminación del _workflow_ de _lint_.
- **Acuerdo 2024-02-06:** Propuestas para nuevos _workflows_. El grupo 2 comenzará a probar algunos de ellos, mientras que el grupo 1 podrá iniciarse también en este proceso.

### ACTA 2024-03

**Asistentes:**

- Barrera Garrancho, María del Carmen
- García Martínez, Carlos
- García Sebastián, Javier
- Meana Iturri, Claudia
- Pérez Gutiérrez, Lucía
- Vento Conesa, Adriana

**Introducción:**

En esta reunión, se definieron los Work Items (WIs) que se implementarán durante el M2 del proyecto. La discusión se centró en la división de estos WIs en tareas más pequeñas y la asignación de responsabilidades entre los miembros del equipo. También se llevó a cabo una lluvia de ideas para cada WI con el fin de definir las mejores formas de implementarlos.

**Acuerdos tomados:**

- **Acuerdo 2024-03-01: Work Items para M2.**  
  Se decidió trabajar en los siguientes WIs para M2:
  - **LOW**:
    - **Remember my password**: Implementación de una funcionalidad que permita a los usuarios recordar su contraseña en caso de olvidarla. Reemplazamos, por tanto, el anterior concepto que teníamos sobre este WI.
    - **Register developer**: Implementación de una opción para que los usuarios puedan registrarse como desarrolladores. Inclusión de características y etiquetas exclusivas para los desarrolladores.
  - **MEDIUM**:
    - **Improve UI**: Rediseño de la interfaz gráfica de usuario para mejorar la experiencia del usuario.

- **Acuerdo 2024-03-02: Divisiones de tareas.**  
  Los WIs seleccionados serán desglosados en tareas más pequeñas, tal como se acordó en la reunión anterior. Cada miembro del equipo tomará tareas relacionadas con diferentes aspectos del proyecto para asegurar que todos trabajen en diversas áreas.

- **Acuerdo 2024-03-03: Lluvia de ideas para implementación de WIs.**  
  Durante la reunión se realizó una lluvia de ideas sobre la implementación de cada WI, con el objetivo de identificar las mejores soluciones y posibles dificultades. Las discusiones incluyeron:
    - **Remember my password**: Se discutieron diversos aspectos de la implementación, como la configuración del servidor de correos, el diseño del frontend y el proceso de generación del código de verificación. Además, se aclaró el alcance de este WI, ya que en reuniones anteriores había dudas sobre su funcionamiento y objetivos específicos.
    - **Register developer**: Se abordaron los campos necesarios para el registro de desarrolladores y cómo integrarlos con el sistema de gestión de usuarios existente. 
    - **Improve UI**: Se discutieron posibles mejoras en el diseño, enfocándose en la usabilidad y la optimización de la navegación.

- **Acuerdo 2024-03-04: Asignación de tareas.**  
  Se asignaron tareas específicas a cada miembro del equipo para asegurar que el progreso fuera adecuado. Las tareas fueron distribuidas según la experiencia y la disponibilidad de cada miembro. Se utilizará la herramienta de gestión de tareas acordada para llevar el seguimiento de cada una de ellas.

### ACTA 2024-04

**Asistentes:**

- Barrera Garrancho, María del Carmen
- García Martínez, Carlos
- García Sebastián, Javier
- Meana Iturri, Claudia
- Pérez Gutiérrez, Lucía
- Vento Conesa, Adriana

**Introducción:**
Durante la reunión se establecieron los Work Items (WIs) que se desarrollarán durante la etapa M3 del proyecto. La conversación se enfocó en dividir cada WI en tareas específicas, buscando un desglose que permita una ejecución ordenada y eficiente. Además, se asignaron responsabilidades entre los miembros del equipo para asegurar que todos trabajen en diversas areas.

**Acuerdos tomados:**

- **Acuerdo 2024-04-01: Work Items para M3.**  
  Se decidió trabajar en los siguientes WIs para M3:
  - **MEDIUM**:
    - **Different versions of models**: Mejora en la funcionalidad que convierte el modelo UVL en diversos formatos al ser cargado, optimizando el rendimiento de la aplicación. 
  - **HIGH**:
    - **Staging area**:  Implementación de una nueva funcionalidad que permita a los usuarios guardar un borrador del conjunto de datos antes de proceder con su publicación definitiva.
    - **Search queries**: Implementación de mejoras como la ampliación de seeders para incluir más datasets o incorporar webscraping, la optimización de la funcionalidad de búsqueda y la adición de una opción para descargar únicamente los datos correspondientes a la consulta, con pruebas asignadas para validar cada aspecto.

- **Acuerdo 2024-04-02: Divisiones de tareas.**  
  Los WIs seleccionados serán desglosados en tareas más pequeñas, tal como se acordó en la reunión anterior. Cada miembro del equipo tomará tareas relacionadas con diferentes aspectos del proyecto para asegurar que todos trabajen en diversas áreas.
- **Acuerdo 2024-04-03: Discusion para implementación de WIs.**  
  Durante la reunión se discutieron diferentes ideas sobre la implementación de cada WI, con el objetivo de identificar las mejores soluciones y posibles dificultades. Las discusiones incluyeron:
    - **Different versions of models**: Se discutió la mejora de la funcionalidad que convierte el modelo UVL en diferentes formatos al ser cargado, optimizando así el rendimiento de la aplicación. Además, se aclaró el alcance de este WI, resolviendo las dudas previas sobre su funcionamiento y objetivos específicos.
    - **Staging area**: Se analizaron diferentes aspectos de la implementación, incluyendo el diseño tanto del backend como del frontend, así como los tests necesarios para garantizar el correcto funcionamiento de la aplicación.
    - **Search queries**: Se discutieron mejoras como la ampliación de seeders para incluir más datasets o incorporar webscraping, la optimización de la funcionalidad de búsqueda y la implementación de una opción para descargar solo los datos correspondientes a la consulta, asignando pruebas para validar cada uno de estos aspectos.

- **Acuerdo 2024-04-04: Asignación de tareas.**  
  Se asignaron tareas concretas a cada miembro del equipo para garantizar un avance óptimo. La distribución de las tareas se basó en la experiencia y disponibilidad de cada persona. Además, se utilizará la herramienta de gestión de tareas previamente acordada para realizar el seguimiento de su progreso.

### ACTA 2024-05

**Asistentes:**

- Barrera Garrancho, María del Carmen
- García Martínez, Carlos
- García Sebastián, Javier
- Meana Iturri, Claudia
- Pérez Gutiérrez, Lucía
- Vento Conesa, Adriana

**Introducción:**
Se llevó a cabo el cierre oficial del proyecto, revisando los aspectos finales y acordando las últimas acciones necesarias para su conclusión exitosa.

**Acuerdos tomados:**

- **Acuerdo 2024-05-01: Finalización del video del proyecto.**
  Se revisaron y aprobaron los detalles finales del video del proyecto. El equipo acordó el cronograma de producción y entrega, confirmando que estará listo para su presentación final.

- **Acuerdo 2024-05-02: Resolución de incidencias.**
  Se discutieron las incidencias pendientes, identificando y resolviendo las últimas cuestiones críticas. Las incidencias menores restantes serán gestionadas de manera interna, sin impacto en el cierre formal del proyecto.

- **Acuerdo 2024-05-03: Cierre de tareas.**
  Se confirmó la finalización de todas las tareas asignadas al equipo. No quedan pendientes por resolver, y se considera que las responsabilidades han sido cumplidas satisfactoriamente.
