# Jamón-Hub - Acta Fundacional

- **Grupo**: G3
- **Nombre del grupo**: jamon-hub-2
- **Tutor**: Jesús Moreno León
- **Curso Escolar**: 2024/2025  
- **Asignatura**: Evolución y Gestión de la Configuración

### Enlaces de interés:

- **Repositorio de código**: [https://github.com/davidgonmar/uvlhub-egc](https://github.com/davidgonmar/uvlhub-egc)  
- **Sistema desplegado**: [https://uvlhub-egc.onrender.com/](https://uvlhub-egc.onrender.com/)

## Índice

1. [Miembros del equipo](#1-miembros-del-equipo)  
2. [Datos fundamentales del equipo](#2-datos-fundamentales-del-equipo)  
   - [Datos de contacto](#datos-de-contacto)  
   - [Work Items a realizar](#work-items-wis-a-realizar)  
3. [Integración con el equipo Jamón-Hub-1](#3-integración-con-el-equipo-jamón-hub-1)  
   - [Motivo de coordinación](#motivo-de-coordinación)  
   - [Work Items a realizar por el grupo 1](#work-items-wis-a-realizar-1)  
   - [Solapamientos de Work Items](#solapamientos-de-work-items-wis)  
4. [Gestión del equipo](#4-gestión-del-equipo)  
   - [Coordinadores del equipo](#coordinadores-del-equipo)  
   - [Comunicación del equipo](#comunicación-del-equipo)  
   - [Toma de decisiones](#toma-de-decisiones)  
   - [Asistencia a milestones](#asistencia-a-milestones)  
   - [Sanciones](#sanciones)  
5. [Gestión del código y la documentación](#5-gestión-del-código-y-la-documentación)  
   - [Alojamiento del código](#alojamiento-del-código)  
   - [Proceso de integración y despliegue continuo](#proceso-de-integración-y-despliegue-continuo)  
   - [Gestión de tareas](#gestión-de-tareas)  
   - [Política de ramas](#política-de-ramas)  
   - [Frecuencia de commits y merge](#frecuencia-de-commits-y-merge)
   - [Cierre de tareas](#cierre-de-tareas)
   - [Mensajes de commits](#mensajes-de-commits)
   - [Títulos de pull requests](#títulos-de-pull-requests)
   - [Versionado del producto](#versionado-del-producto)
6. [Gestión de Work Items](#6-gestión-de-work-items-wis)
   - [Asignación de actividades](#asignación-de-actividades)
   - [Tipos de issues](#tipos-de-issues)
   - [Roles en issues](#roles-en-issues)
   - [Priorización de issues](#priorización-de-issues)
   - [Estados de issues](#estados-de-issues)
   - [Etiquetas de issues](#etiquetas-de-issues)
   - [Nomenclatura de issues](#nomenclatura-de-issues)
   - [Estandarización de incidencias](#estandarización-de-incidencias)
7. [Declaración final de compromisos](#7-declaración-final-de-compromisos)

---

## 2. Datos fundamentales del equipo

### Datos de contacto:

| **Nombre Completo**                | **UVUS**    | **Email**                        | **GitHub User** |
|------------------------------------|------------|----------------------------------|---------------------|
| Barrera Garrancho, María del Carmen | marbargar8 | marbargar8@alum.us.es            | Playeira01          |
| García Martínez, Carlos            | cargarmar18 | cargarmar18@alum.us.es           | Cargarmar18         |
| García Sebastián, Javier           | javgarseb  | javgarseb@alum.us.es             | JaviGarcia1           |
| Meana Iturri, Claudia              | clameaitu  | clameaitu@alum.us.es             | clameaitu           |
| Pérez Gutiérrez, Lucía             | lucpergut  | lucpergut@alum.us.es             | LuciaPG           |
| Vento Conesa, Adriana              | adrvencon  | adrvencon@alum.us.es             | adrvencon           |


### Work Items (WIs) a realizar:

#### **HIGH**:
- **Staging Area**: Implementación de un espacio temporal que permite a los usuarios almacenar datasets antes de ser subidos a Zenodo.  
- **Search Queries**: Desarrollo de funcionalidades avanzadas que permiten a los usuarios realizar consultas específicas para filtrar y descargar modelos según criterios personalizados.

#### **MEDIUM**:
- **Improve UI**: Rediseño y optimización de la interfaz gráfica de usuario para mejorar la experiencia del usuario. La visualización de los datasets debe ser similar a la de GitHub.
- **Different versions of models**: Soporte para diferentes versiones de modelos y su descarga en varios formatos.

#### **LOW**:
- **Remember my password**: Integración de una funcionalidad que permite a los usuarios optar por guardar su contraseña, facilitando el acceso a la aplicación sin la necesidad de ingresarla repetidamente.
- **Register developer**: Opción para que los usuarios se registren como desarrolladores.
---

## 3. Integración con el equipo Jamón-Hub-1

### Motivo de coordinación:

Los equipos Jamón-Hub-1 y Jamón-Hub-2 ya han trabajado juntos antes y han conseguido buenos resultados. Ambos equipos acordaron colaborar para maximizar el éxito en el proyecto.

### Work Items (WIs) a realizar:

#### **HIGH**:
- **AI Integration**: Implementación de una AI (OpenAI) en UVLHub.
- **Advanced Search**: Funcionalidad de búsqueda avanzada que permitirá a los usuarios filtrar modelos según criterios específicos.

#### **MEDIUM**:
- **Download all datasets**: Opción que permitirá a los usuarios descargar todos los datasets disponibles en múltiples formatos con un solo clic.
- **Rate datasets/models**: Función que habilitará a los usuarios para evaluar y dejar valoraciones sobre los datasets y modelos.

#### **LOW**:
- **Sign-up validation**: Proceso de validación del correo electrónico durante el registro de usuarios.
- **Multiple login**: Opción para que los usuarios inicien sesión utilizando sus cuentas de ORCID, GitHub o Google.

### Solapamientos de Work Items (WIs):

Al coordinarse ambos equipos, se identificaron múltiples conflictos y solapamientos en los **Work Items** (WIs), especialmente en los siguientes:
  
- **Advanced Search** (grupo 1) vs. **Search Queries** (grupo 2): Ambos WIs se centran en la búsqueda y filtrado de modelos, lo que puede generar conflictos en la implementación de criterios de búsqueda.
  
- **Sign-up Validation**, **Multiple Login**, **Remember My Password**, y **Register Developer**: Estos WIs, que giran en torno a la autenticación, afectan a los módulos `auth` y `profile`. La coordinación entre los grupos es fundamental para evitar duplicaciones y asegurar la cohesión en la funcionalidad de autenticación.

- **Improve UI**: Las mejoras visuales propuestas en este WI pueden impactar en la interfaz de otras funcionalidades, como los botones de descarga en *Download All Datasets* y el sistema de valoración en *Rate Datasets/Models*, lo que puede llevar a inconsistencias visuales si no se gestionan adecuadamente.

- **Different Versions of Models**, **Search Queries** y **Download All Datasets**: Estos tres WIs están interconectados en términos de descarga y manejo de datasets. *Different Versions of Models* establece el proceso de conversión a diferentes formatos, *Search Queries* permite seleccionar modelos específicos, y *Download All Datasets* facilita la descarga de todos los formatos. La implementación de estos WIs debe realizarse de forma coordinada para asegurar que se reutilicen las funcionalidades desarrolladas en cada uno.

---

## 4. Gestión del equipo

### Coordinadores del equipo:

- **Coordinador principal**: Adriana Vento Conesa 
- **Coordinador secundario**: Lucía Pérez Gutiérrez

### Comunicación del equipo:

- **Plataforma principal**: WhatsApp y Discord
- **Reuniones**: Presenciales o mediante Discord, con registro en el "Diario del equipo".  
- **Comunicación con los profesores**: Correo electrónico vía Microsoft Outlook.

### Toma de decisiones:

Las decisiones se tomarán por mayoría absoluta del equipo. En caso de no alcanzar un consenso, se recurrirá al profesor para obtener orientación. Para las decisiones que involucren al grupo 2, los coordinadores se encargarán de gestionar la comunicación. 

### Asistencia a milestones:

El grupo ha acordado asistir a los hitos (*milestones*) en el horario del G3. 

### Sanciones:

| **Conflicto**                                                   | **Acción a realizar**                                                                                                            |
|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| **Falta de interés y rendimiento**                            | - **Motivación y apoyo:** Se llevará a cabo una charla individual con los miembros con bajo rendimiento para entender sus preocupaciones y motivaciones. <br> - **Seguimiento:** Si la situación persiste, se considerará la privación de voto en decisiones del equipo como última opción.                                   |
| **Ausencia injustificada en milestones**                      | - **Evaluación inicial:** Se mantendrá una actitud positiva en el equipo, pero se establecerán límites claros. <br> - **Sanciones:** En caso de ausencia injustificada, se procederá a documentar la situación y comunicarla al coordinador para evaluar la posible baja del miembro.                  |
| **Falta de participación en reuniones**                       | - **Recordatorios:** Se enviarán recordatorios y se establecerán agendas claras para cada reunión. <br> - **Consulta:** Si un miembro no asiste repetidamente, se llevará a cabo una conversación privada para identificar obstáculos y buscar soluciones.                             |
| **Desacuerdos sobre el enfoque del trabajo**                 | - **Facilitación de discusión:** Se fomentará un espacio abierto para que los miembros expresen sus puntos de vista y se discutirá cada opinión en un ambiente respetuoso. <br> - **Mediación:** Si no se llega a un acuerdo, se considerará la intervención del coordinador para facilitar el diálogo y llegar a una solución conjunta.                                |
| **Diferencias en habilidades e interés entre miembros**      | - **Identificación de talentos:** Se identificarán las fortalezas de cada miembro y se asignarán roles que maximicen sus habilidades. <br> - **Mentoría:** Los miembros más experimentados ofrecerán apoyo a aquellos que necesiten orientación. <br> - **Capacitación:** Se podrán organizar sesiones de formación para nivelar el conocimiento del equipo.                               |
| **Repetición de conflictos menores**                          | - **Documentación:** Se mantendrá un registro de los conflictos menores en el acta funcional. <br> - **Reuniones de seguimiento:** Se organizarán reuniones periódicas para evaluar el clima del equipo y abordar cualquier tensión antes de que se convierta en un problema mayor. |

---

## 5. Gestión del código y la documentación

### Alojamiento del código:

El repositorio se alojará en GitHub, utilizado por ambos equipos para facilitar la integración continua.

### Proceso de integración y despliegue continuo:

1. El código se almacenará en un único repositorio remoto.  
2. Los builds se automatizarán con herramientas de Git.  
3. Los commits se realizarán con frecuencia para asegurar la integración continua.  
4. Todos los commits lanzarán trabajos de CI.  
5. Las pruebas se realizarán en un entorno de preproducción.  
6. Los cambios en la rama "main" dispararán la CD para desplegar automáticamente la nueva versión.

### Gestión de tareas:

Se utilizarán **Issues** y **Projects** de GitHub para gestionar las tareas. Cada equipo tendrá su propio *Project* para organizar y asignar responsables.

### Política de ramas:
Dado que GitFlow no es una opción viable, el equipo ha decidido adoptar un enfoque alternativo: crear una rama para cada tarea a realizar. Salvo excepciones, las ramas seguirán los siguientes patrones:

Si son tareas:
```
g2/task_<número_de_tarea>/<nombre_de_ticket>
```

Si son incidencias:
```
g2/incidence_<número_de_tarea>/<nombre_de_issue>
```

La sección "*g2*" se utiliza para diferenciar las ramas del grupo 2 de aquellas del grupo 1. Por ejemplo, una rama podría verse así:

```
g2/task_328/cambiar_tipografía
```

Entre las excepciones, se incluye la rama "main", que funcionará como la rama principal destinada al despliegue, la rama "build", que se empleará para realizar cambios específicos en la configuración del entorno y la rama g2/documentation, que se usará para añadir la documentación del grupo 2.

### Frecuencia de commits y merge:

Con el propósito de facilitar la integración continua, el equipo ha acordado realizar un mínimo de un commit cada tres días naturales, excluyendo el sábado y el domingo. El _commit_ ha de incluir todos los cambios listos para producción. Si ningún cambio está listo para ser integrado y desplegado, se permite realizar un commit vacío. Los cambios listos para producción se integrarán a la rama "main" con la misma frecuencia.

### Cierre de tareas:

El encargado de una tarea creará sus propias _pull requests_. Él mismo, o en su defecto, los coordinadores, asignarán a un revisor entre los miembros del proyecto, para revisar cualitativamente el contenido de la misma y el cumplimiento con los requisitos.

Si el revisor aprueba la _pull request_, éste se encargará en el momento de hacer _merge_. Si no la aprueba, el revisor dejará abierta la _pull request_, y escribirá sus comentarios en ella. Se notificará al encargado de la tarea para que revise los errores. Una vez supuestamente arreglados, los cambios aparecerán en la misma _pull request_, y se volverá a empezar este ciclo.

Una vez se le ha hecho _merge_ a una tarea y se ha cerrado, el encargado de la tarea para la cual se ha creado la rama, se encargará de borrar la rama.

### Mensajes de commits:

El proyecto utilizará [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), una especificación que tiene como objetivo hacer que los mensajes de commit sean legibles tanto para humanos como para máquinas. La información correspondiente a este apartado se ha extraído de la página oficial. Por lo tanto, los commits deben seguir la siguiente estructura, y deberán escribirse en inglés mayoritariamente:

```xml
      <type>(<scope>): <subject>
      <BLANK LINE>
      <body>
      <BLANK LINE>
      <footer>
```

- `<type>` se refiere a uno de los varios tipos preestablecidos de operaciones que se pueden realizar en el proyecto. Este atributo es **requerido**. Los tipos recomendados y su uso son:
   - `feat`: Nueva funcionalidad.
   - `fix`: Corrección de errores.
   - `docs`: Cambios solo en la documentación.
   - `style`: Cambios que no afectan el significado del código (espacios en blanco, formato, punto y coma faltante, etc.).
   - `refactor`: Un cambio de código que no corrige un error ni agrega una funcionalidad.
   - `perf`: Un cambio de código que mejora el rendimiento.
   - `test`: Modificaciones en el banco de pruebas.
   - `chore`: Cambios en el proceso de construcción o en herramientas auxiliares y bibliotecas, como la generación de documentación.
   - `revert`: Reversión de uno o más commits.

- `<scope>` es cualquier cosa que especifique el lugar del cambio del commit. Este atributo es opcional. Por ejemplo, `api`, `lang`, o `owner`.

- `<subject>` contiene el mensaje del commit, o en otras palabras, la descripción corta del cambio realizado. Este atributo es **requerido**. Se usará minúscula al comienzo, y no se usará punto al final. Empezaremos por un verbo en imperativo, a poder ser.

- `<body>` contiene una explicación más detallada de la motivación del cambio y/o cómo este contrasta con el código anterior. Este atributo es opcional.

- `<footer>` contiene cualquier información extra, como cambios importantes en la API o referencias a problemas de GitHub o commits. Incluirá el ID de la issue (si procede), para poder relacionar el commit con ella.

**Ejemplo**:

```
feat(user-profile): add profile picture in backend

It adds a new feature that allows users to upload prophile pictures by themselves.
This commit includes the backend implementation. The frontend one will be made soon.

#12
```

Se hará uso de un *hook* para controlar que no se realiza un commit con mensaje erróneo.

### Títulos de pull requests:

Por motivos de claridad y unificación, el equipo ha definido un formato para el nombramiento de las _pull requests_. No es un formato fijo, sino que se basa en los siguientes principios:

 - No se usará el nombre por defecto que provee GitHub, el cual parsea el nombre de la rama de origen.
 - No se usará el formato de Conventional Commits (es decir, el texto por defecto del commit).
 - Será una descripción breve y sin adornos del objetivo de la _pull request_. Se ha de asemejar en parte al título de la _issue_ a la que corresponde, si procede.

### Versionado del producto:

El proyecto seguirá las directrices de [versionado semántico](https://semver.org/). La información correspondiente a este apartado se ha extraído de la página oficial. Por lo tanto, el versionado funcionará de la siguiente manera:

- **Versión mayor**: Este número se incrementa cuando se realizan cambios significativos e incompatibles en la API del proyecto. Indica que la nueva versión puede no ser compatible con las versiones anteriores y requiere una cuidadosa consideración durante las actualizaciones. (**Ejemplo:** 2.0.0 -> 3.0.0)

- **Versión menor**: Incrementar este número significa la adición de nuevas funcionalidades al proyecto de manera compatible con versiones anteriores. Los usuarios pueden esperar que las características existentes se mantengan intactas, lo que garantiza transiciones suaves entre versiones. (**Ejemplo:** 2.0.0 -> 2.2.0)

- **Parche**: Los incrementos en la versión de parche están reservados para correcciones de errores que son compatibles con versiones anteriores. Estos cambios abordan problemas sin introducir nuevas funcionalidades o romper la funcionalidad existente, proporcionando a los usuarios una experiencia fluida durante las actualizaciones. (**Ejemplo:** 2.0.0 -> 2.0.2)

---

## 6. Gestión de Work Items (WIs)

### Asignación de actividades:
Al inicio de cada sprint, el equipo descompondrá los Work Items (WIs) en actividades específicas, las cuales serán asignadas entre los miembros del equipo. Se buscará equilibrar la carga de trabajo en términos de tiempo y esfuerzo, aprovechando al máximo las habilidades e intereses individuales.

### Tipos de issues:
Una _issue_ representará una solicitud de cambio en el sistema. Los tipos de _issues_ que se gestionarán son:

- **Actividades derivadas de WIs:** creadas por el equipo durante la planificación para cumplir con los _Work Items_.
  - **Tarea:** actividad principal necesaria para completar un WI.
- **Incidencias:** reportadas por el equipo o usuarios para notificar problemas en el funcionamiento del sistema.

Las actividades de documentación, como la actualización del 'Diario del equipo' no se representará mediante issues.

A las issues generadas automáticamente por bots no se les aplicarán estas políticas.

### Roles en issues:
Cada _issue_ será asignada a un único miembro del equipo, quien será responsable de su ejecución. En caso de que se necesite involucrar a más personas, se creará una _issue_ adicional para repartir el trabajo.

### Priorización de issues:
Se utilizará la siguiente clasificación para definir la prioridad de las _issues_:

- **Alta:** Tareas críticas para el progreso del proyecto. Estas tareas afectan directamente el avance, ya que otras tareas dependen exclusivamente de su finalización.
- **Media:** Tareas que tienen una doble función: dependen de otras tareas para empezar o completarse y, al mismo tiempo, otras tareas dependen de ellas. Son importantes, pero no bloquean el progreso de manera inmediata.
- **Baja:** Tareas independientes que no tienen ninguna otra tarea que dependa de ellas. Su ejecución no afecta directamente el avance del proyecto.

### Estados de issues:
Las _issues_ pasarán por los siguientes estados. En GitHub Projects, estos se representarán mediante columnas.

| Estado           | Descripción                                                                                         |
|------------------|-----------------------------------------------------------------------------------------------------|
| **_TODO_**           | Tareas que aún no han comenzado. |
| **_In Progress_**    | Tareas que estén en proceso.                                                    |
| **_Failed Pull Request_**      | Tareas cuya _pull request_ no ha sido aprobada.                                                   |
| **_Done_**           | Tareas que han sido aprobadas o completadas.                                    |

Si una pull request no se acepta, e trasladará a la columna del estado _Failed Pull Request_. Una vez que las correcciones sean realizadas, pasará al estado _Done_.

### Etiquetas de issues:
Las siguientes etiquetas se utilizarán para clasificar los cambios en las _issues_:

- Tipos de actividad: `task`, `incidence`.
- Tipo de cambio: `documentation`, `feat`, `fix`, `refactor`, `style`, `test`, `database`, `meeting`, `build`, `deployment` y `hotfix`.
- Áreas del sistema: `backend`, `frontend`.

### Nomenclatura de issues:

Para mantener un orden coherente, los títulos de las **issues** seguirán los siguientes patrones:
```
Tarea <número_tarea>-<número_subtarea_(opt)>: <Nombre_tarea>.
```
Ejemplos:

```
Tarea 13-1: Cambiar diseño de botones.
```

```
Tarea 15: Realizar tests de login.
```

El cuerpo seguirá la siguiente estructura:

```html
Work item:
>  <work item al que pertenece si procede>
Description:
>  - <primer punto>
>  - <segundo punto>
>  [...]
```
> El símbolo ">" se parseará en el markdown de la descripción de las issues en GitHub tal y como se ve en este comentario.

Ejemplo:

```html
Work item:
>  Sign-up validation
Description:
>  - Notify the user, onscreen, that an email has been sent.
>  - Wait for the code to be sent and send it one it is entered.
``` 

Se hará a través de una plantilla de tareas en GitHub.

### Estandarización de incidencias:
Para garantizar que las incidencias reportadas contienen la información necesaria para su resolución, se seguirá esta plantilla:

```html
   Título
      <título de la incidencia>
   Descripción
      <descripción>
   Pasos para reproducir
      1. <primer paso>
      2. <segundo paso>
      [...]
   Resultado esperado
      <resultado esperado>
   Resultado obtenido
      <resultado obtenido>
   Evidencias (capturas, logs, etc.)
      <evidencias>
   Entorno
      - Sistema operativo: <sistema operativo>
      - Versión del producto: <versión del producto>
      - Navegador:
         - Modelo: <modelo de navegador>
         - Versión: <versión del navegador>
      - Detalles adicionales: <detalles adicionales>
   Posibles soluciones:
      <ideas sobre cómo solucionar el problema>
   Percepción de prioridad o severidad (crítica, alta, media o baja):
      <percepción sobre la prioridad o severidad de la incidencia>
   Comentarios adicionales
      <comentarios adicionales>
```

Se hará a través de una plantilla de incidencias en GitHub.

---

## 7. Declaración final de compromisos

Con la publicación de este acta, los miembros del equipo Jamón-Hub-2 reconocen haber leído y entendido todos los acuerdos y compromisos aquí establecidos, y se comprometen a cumplir con lo pactado para asegurar el éxito del proyecto.

### Firmas de los miembros del equipo:

| **Nombre Completo**                | **UVUS**     | **Firma** | **Fecha**     |
|------------------------------------|--------------|-----------|---------------|
| Vento Conesa, Adriana              | adrvencon    | ✓         | 17/10/2024    |
| Meana Iturri, Claudia              | clameaitu    | ✓         | 17/10/2024    |
| Pérez Gutiérrez, Lucía             | lucpergut    | ✓         | 17/10/2024    |
| García Martínez, Carlos            | cargarmar18  | ✓         | 17/10/2024    |
| García Sebastián, Javier           | javgarseb    | ✓         | 17/10/2024    |
| Barrera Garrancho, María del Carmen | marbargar8  | ✓         | 17/10/2024    |

> **Nota:** Al firmar, cada miembro acepta los términos y condiciones establecidos en este acta y se compromete a trabajar en colaboración para alcanzar los objetivos del proyecto.

---
