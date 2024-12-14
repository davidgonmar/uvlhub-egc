# Documento del Proyecto

- **Grupo**: G3
- **Nombre del grupo**: jamon-hub-2
- **Tutor**: Jesús Moreno León
- **Curso Escolar**: 2024/2025  
- **Asignatura**: Evolución y Gestión de la Configuración

## Índice

1. [Indicadores del Proyecto](#indicadores-del-proyecto)  
2. [Integración con Otros Equipos](#integración-con-otros-equipos)  
3. [Resumen Ejecutivo](#resumen-ejecutivo)  
4. [Descripción del Sistema](#descripción-del-sistema)
    - [1. Vistazo general](#1-vistazo-general)
    - [2. Módulos](#2-módulos)
    - [3. Estructura del proyecto](#3-estructura-del-proyecto)
    - [4. Peticiones HTTP](#4-peticiones-http)
    - [5. Añadidos al proyecto](#5-añadidos-al-proyecto)   
5. [Visión Global del Proceso de Desarrollo](#visión-global-del-proceso-de-desarrollo)  
    - [Introducción](#1-introducción)  
    - [Fases del proceso de desarrollo](#2-fases-del-proceso-de-desarrollo)  
        - [Fase de planificación](#fase-de-planificación)  
        - [Fase de diseño](#fase-de-diseño)  
        - [Fase de desarrollo](#fase-de-desarrollo)  
        - [Fase de pruebas](#fase-de-pruebas)  
        - [Fase de despliegue](#fase-de-despliegue)  
        - [Fase de mantenimiento](#fase-de-mantenimiento)
    - [Ejercicio de Cambio Propuesto](#3-ejercicio-de-cambio-propuesto)  
7. [Entorno de Desarrollo](#entorno-de-desarrollo)  
    - [Entornos de desarrollo utilizados](#entorno-de-desarrollo-utilizado)  
    - [Métodos de instalación](#métodos-de-instalación)  
        - [Instalación manual](#1-instalación-manual)  
        - [Instalación con Docker](#2-instalación-con-docker)  
        - [Instalación con Vagrant](#3-instalación-con-vagrant)
8. [Ejercicio de Propuesta de Cambio](#ejercicio-de-propuesta-de-cambio)  
   - [Planificación](#1-planificación)  
   - [Desarrollo](#2-desarrollo)  
   - [Pruebas](#3-pruebas)  
   - [Creación de la Pull Request](#4-creación-de-la-pull-request)  
   - [Despliegue](#5-despliegue)  
   - [Mantenimiento](#6-mantenimiento)
9. [Conclusiones y Trabajo Futuro](#conclusiones-y-trabajo-futuro)  

---

El presente documento tiene como objetivo sintetizar los aspectos clave del proyecto elegido para su desarrollo, en relación con los temas abordados durante las clases. En él, se identifican claramente los miembros del equipo, los grupos a los que pertenecen, el curso académico, y el nombre del proyecto, siguiendo la política de nomenclatura establecida. 

## Indicadores del Proyecto

| Miembro del equipo                             | Horas | Commits | LoC  | Test | Issues | Work Item         |
|------------------------------------------------|-------|---------|------|------|--------|-------------------|
| [Barrera Garrancho, María del Carmen](https://github.com/Playeira01) | HH    | XX      | YY   | ZZ   | II     | Descripción breve |
| [García Martínez, Carlos](https://github.com/Cargarmar18)            | HH    | XX      | YY   | ZZ   | II     | Descripción breve |
| [García Sebastián, Javier](https://github.com/JaviGarcia1)           | HH    | XX      | YY   | ZZ   | II     | Descripción breve |
| [Meana Iturri, Claudia](https://github.com/clameaitu)               | 64    | 51      | +1865 -1182   | 12   | 5     | Improve Search Queries: changed search to static, can now download all datasets in a zip that appear in a search query |
| [Pérez Gutiérrez, Lucía](https://github.com/LuciaPG)                | HH    | XX      | YY   | ZZ   | II     | Descripción breve |
| [Vento Conesa, Adriana](https://github.com/adrvencon)               | HH    | XX      | YY   | ZZ   | II     | Descripción breve |
| **TOTAL**                                       | tHH   | tXX     | tYY  | tZZ  | tII    | Descripción breve |

A continuación se detallan las fuentes para obtener las métricas clave del proyecto:

- **Horas trabajadas**: 
  - GitHub no ofrece un registro directo de las horas trabajadas por cada miembro del equipo. Para el seguimiento de tiempo, utilizamos Clockify. Las métricas de horas trabajadas se basan en los informes y gráficos generados internamente por Clockify.
- **Commits**:
  - Se pueden ver los **commits** realizados en el repositorio. Este historial incluye todos los cambios hechos por los miembros del equipo. El historial de commits se eliminó al inicio del proyecto.
    - Enlace: [Historial de Commits](https://github.com/davidgonmar/uvlhub-egc/commits) o [Estadísticas de Commits](https://github.com/davidgonmar/uvlhub-egc/graphs/contributors)
- **Líneas de Código (LoC)**:
  - Para contar las líneas de código producidas por el equipo, utilizamos el **Insights** de GitHub.
    - Enlace: [Estadísticas de Líneas de Código](https://github.com/davidgonmar/uvlhub-egc/graphs/contributors)
- **Test**:
  - Los tests realizados por el equipo no tienen una métrica directa en GitHub, pero pueden ser encontrados en el código fuente o en los resultados de integración continua a través de **GitHub Actions**.
    - Enlace para revisar los **resultados de test en GitHub Actions**: [GitHub Actions Tests](https://github.com/davidgonmar/uvlhub-egc/actions/workflows/tests.yml)
- **Issues gestionadas**:
  - Enlace: [Issues en GitHub](https://github.com/davidgonmar/uvlhub-egc/issues)
    - Se puede filtrar por etiquetas, autor o estado de la issue (abierta/cerrada) para ver la gestión de las tareas e incidencias.
- **Work Items**:
  - Los work items del proyecto se asocian con las **Issues** en GitHub. Aunque cada miembro del equipo ha dedicado más tiempo a ciertos WI que a otros, todos han participado activamente en diversas tareas relacionadas con diferentes WI. Este enfoque busca promover un ambiente colaborativo, favoreciendo la revisión continua y el trabajo en equipo para alcanzar los objetivos del proyecto de manera eficiente.
    - Enlace: [Issues en GitHub](https://github.com/davidgonmar/uvlhub-egc/issues)

## Integración con Otros Equipos

Equipos con los que se ha integrado y los motivos por los que lo ha hecho y lugar en el que se ha dado la integración:

- **Jamon-Hub-1**: La integración con este equipo se dio para coordinar los solapamientos de funcionalidad en los **Work Items** (WIs) identificados. Los WIs de ambos equipos tenían puntos de intersección que requerían una estrecha colaboración para garantizar una implementación coherente y evitar conflictos en la funcionalidad del proyecto. La integración se dio principalmente en los módulos de autenticación, búsqueda y descarga de datasets, así como en la mejora de la interfaz de usuario. Los puntos clave de solapamiento fueron los siguientes:
  
  - **Advanced Search**  y **Search Queries**: Ambos WIs se enfocaban en la búsqueda y filtrado de modelos, lo que generaba conflictos en la implementación de los criterios de búsqueda.
  
  - **Sign-up Validation**, **Multiple Login**, **Remember My Password**, y **Register Developer**: Estos WIs, relacionados con la autenticación, impactaban en los módulos `auth` y `profile`. La coordinación entre los equipos fue esencial para evitar duplicaciones y asegurar la coherencia en la funcionalidad de autenticación y envío de emails.

  - **Different Versions of Models**, **Search Queries** y **Download All Datasets**: Estos tres WIs estaban interconectados en términos de la descarga y manejo de datasets. *Different Versions of Models* establecía el proceso de conversión a diferentes formatos, *Search Queries* permitía seleccionar modelos específicos, y *Download All Datasets* facilitaba la descarga de todos los formatos. La implementación coordinada de estos WIs fue crucial para asegurar que se reutilizaran las funcionalidades desarrolladas en cada uno.

  - **Fakenodo**: La implementación de *Fakenodo* fue un trabajo colaborativo entre los dos grupos. El grupo 2 se encargó de desarrollar la funcionalidad principal, mientras que el grupo 1 se centró en las pruebas, ajustes finales y la corrección de errores. Esta colaboración permitió entregar una solución funcional.

Esta integración se dio en un esfuerzo por optimizar el flujo de trabajo entre los equipos, mejorar la cohesión del proyecto y garantizar la calidad del producto final.

## Resumen Ejecutivo

El proyecto ha sido desarrollado como parte del curso universitario EGC por el grupo Jamon-Hub, compuesto por los subgrupos Jamon-Hub-1 y Jamon-Hub-2, tiene como objetivo la mejora del proyecto UVLHub mediante la incorporación de nuevas funcionalidades y el cumplimiento de los principios de integración continua (CI) y despliegue continuo (CD). Se ha realizado un especial énfasis en la gestión del código y su evolución.

Esta aplicación es un fork de la original, a la cual se le han añadido mejoras significativas y funcionalidades innovadoras a la vez que se han mantenido la inmensa mayoría de sus características. Estas mejoras buscan optimizar la experiencia de usuario mejorando la versatilidad, funcionalidad y comodidad del sistema. A continuación, se detalla el alcance del trabajo realizado por cada subgrupo:

El subgrupo Jamon-Hub-1 ha implementado las siguientes funcionalidades:

- **AI Integration:** implementación de un sistema de inteligencia artificial basado en OpenAI mediante una API externa, que permite a los usuarios consultar información sobre modelos UVL.
- **Advanced Search:** adición de una funcionalidad de búsqueda avanzada para que los usuarios puedan filtrar modelos según criterios específicos.
- **Download All Datasets:** desarrollo de una opción que permite descargar todos los *datasets* disponibles en todos los formatos mediante un único botón.
- **Rate Datasets/Models:** implementación de una funcionalidad que permite a los usuarios valorar tanto *datasets* como modelos.
- **Sign-up Validation:** implementación de un sistema de validación de correo electrónico como parte del proceso de registro de nuevos usuarios.
- **Multiple Login:** integración de opciones de inicio de sesión utilizando cuentas de ORCID, GitHub o Google.
- **Fakenodo:** desarrollo de un stub que simula la funcionalidad de la API de Zenodo, permitiendo la prueba y el uso del sistema sin depender de servicios externos reales. Esta tarea ha sido desarrollada en colaboración con Jamon-Hub-2.

El subgrupo Jamon-Hub-2 ha desarrollado las siguientes funcionalidades:

- **Staging Area:** implementación de un área temporal para que los usuarios almacenen datasets antes de subirlos definitivamente a Zenodo.
- **Search Queries:** desarrollo de herramientas avanzadas que permiten realizar consultas específicas para filtrar y descargar modelos según criterios personalizados.
- **Improve UI:** optimización del diseño de la interfaz de usuario, mejorando la experiencia visual y funcional. La presentación de los datasets sigue un estilo inspirado en GitHub.
- **Different Versions of Models:** soporte para la gestión de diferentes versiones de modelos y su descarga en varios formatos.
- **Remember (Forgot) My Password:** creación de una funcionalidad que permite a los usuarios modificar sus contraseñas en caso de olvido u otra causa.
- **Register Developer:** adición de una opción para que los usuarios puedan registrarse como desarrolladores y acceder a funcionalidades específicas.
- **Fakenodo:** desarrollo de un stub que simula la funcionalidad de la API de Zenodo, permitiendo la prueba y el uso del sistema sin depender de servicios externos reales. Esta tarea ha sido desarrollada en colaboración con Jamon-Hub-1.

Cada una de estas funcionalidades ha sido diseñada y desarrollada siguiendo las mejores prácticas de desarrollo ágil y de evolución y gestión de la configuración, para asegurar la mayor calidad posible del resultado final. En esta misma línea, se ha aportado un cuidado especial a la coordinación entre los dos equipos para garantizar una cooperación efectiva y evitar conflictos de alto impacto.

Entre las técnicas llevadas a cabo para lograr dichas metas, destacan la definición y aplicación de políticas de formato de *issues*, ramas, commits y *pull requests*, y el empleo de *workflows* de automatización de procesos. Todo esto se puede leer en detalle en los actas fundacionales de cada grupo.

El resultado es un proyecto robusto que, con humildad pero confianza, espera haber superado al original, ofreciendo una experiencia más rica y adaptada a las posibles necesidades de los usuarios.

## Descripción del Sistema

UVLHub es un repositorio de modelos de características en formato UVL siguiendo principios de ciencia abierta. Vamos a ver a continuación una descripción del sistema desde el punto de vista funcional y arquitectónico. Se analizarán sus componentes y su relación con el resto de subsistemas.

> **Aviso**: Esta información ha sido parcialmente obtenida de [la documentación oficial del proyecto original clonado](https://docs.uvlhub.io/). Consúltese para más información.

### 1. Vistazo general

![Overview of UVLHub architecture](https://imgur.com/lSoYBlK.png)

#### Aplicación web
UVLHub está desarrollada como una aplicación web mediante el framework Flask. Su principal punto de acceso es un navegador web. Adicionalmente, UVLHub integra cuatro servicios distintos: almacenaje local para modelos UVL y demás información pertinente (2), Zenodo para persistencia de los datos (3), análisis automático de modelos de características (Automated Analysis of Feature Models - AAFM) mediante Flamapy (4), y un servicio RESTful para extender sus funcionalidades a otros dominiones mediante API (5).

#### Almacenaje local
Los usuarios pueden subir modelos en el formato UVL. Los archivos *per se* son almacenados en local, mientras que la información relacionada, tal como el título, la descripción y los autores, es guardada en una base relacional.

#### Zenodo
Zenodo es un repositorio de acceso abierto que permite a investigadores, científicos, académicos y cualquier persona interesada en compartir sus investigaciones cargar y almacenar datos de investigación, publicaciones, software y otros resultados científicos. 

A pesar de guardar los archivos en local, también se suben al repositorio general de Zenodo como medio de seguridad. De este modo, si UVLHub no estuviese disponile, siempre se podrán hallar en Zenodo, permitiendo restaurar los datos sin pérdidas.

#### AAFM mediante Flamapy
Los usuarios pueden analizar sintácticamente sus modelos de UVLHub. Este análisis llevado a cabo mediante la herramienta Flamapy puede determinar, por ejemplo, la validez del modelo, el recuento de características o la cantidad de productos diferentes que se pueden derivar del modelo.

#### API REST
UVLHub ofrece una API REST gratis accesible para cualquier usuario registrado como desarrollador, para poder integrar en dominios externos modelos validados de la aplicación.

### 2. Módulos

![Modules of UVLHub](https://imgur.com/ksuWJOj.png)
*La imagen de arriba representa la estructura y relación de los módulos del proyecto UVLHub original, previo a los añadidos de este proyecto.*

<br>
Las funcionalidades de UVLHub están desglosadas en módulos. Cada módulo incluye las características fundamentales de un concepto funcional, de modo que cada uno sea cohesivo, esté desacoplado de los demás, sea modular y sea reutilizable. Las funcionalidades serán fruto de la relación entre módulos.

Dentro de un módulo podemos encontrar los formularios (*forms*), los modelos de datos, los repositorios, las rutas de controladores, los *seeders* de datos, los servicios, las plantillas (*templates*) de las páginas de frontend, y las pruebas (*tests*).

Actualmente esta aplicación UVLHub cuenta con 14 módulos. A continuación se listan todos en orden alfabético, aportando una descripción para cada uno:

- **Auth:** para la autenticación.
- **Chatbot:** para la implementación de un sistema de inteligencia artificial basado en OpenAI mediante una API externa, que permite a los usuarios consultar información sobre modelos UVL.
- **Dataset:** para gestionar conjuntos de modelos UVL, llamados *datasets*.
- **Explore:** para poder explorar las diferentes modelos y *datasets*.
- **Fakenodo:** stub que simula la funcionalidad de la API de Zenodo, permitiendo la prueba y el uso del sistema sin depender de servicios externos reales.
- **Feature Model:** para gestionar modelos UVL.
- **Flamapy:** para incorporar las funcionalidades de Flamapy para el análisis automático de modelos de características (AAFM).
- **Hubfile:** para gestionar el conjunto de los *datasets* de los usuarios.
- **Notepad:** función de hojas de notas añadida como ejemplo simple de funcionalidad.
- **Profile:** para gestionar el perfil de un usuario.
- **Public:** para mostrar la página principal de la aplicación.
- **Team:** para mostrar el equipo de desarrolladores encargados de la aplicación.
- **Webhook:** para ejecutar el despliegue del webhook de la aplicación.
- **Zenodo:** para acceder a la API de Zenodo y realizar acciones tales como publicar modelos de UVL.

### 3. Estructura del proyecto

![Structure of UVLHub](https://imgur.com/UARumxi.png)
*La imagen de arriba representa la los componentes del código fuente del proyecto UVLHub original, previo a los añadidos de este proyecto.*

<br>
La estructura del código fuente del proyecto se puede agrupar de forma lógica en los siguientes componentes:

#### Configuración del repositorio
En este componente tendríamos la carpeta `.github`, el archivo `.gitignore`, la carpeta `documentation` y el archivo `README`.md.

- **.github:** dentro se encuentra la carpeta `workflows` la cual define los GitHub Actions *workflows*. Estos archivos YAML dfinen acciones automatizadas que son ejecutados tras ciertos sucesos, tales como *pushes* o *pull requests*.
- **.gitignore:** una lista de archivos y directorios que Git debe ignorar de su sistema de control de versiones.
- **documentation:** contiene el acta fundacional, el diario del equipo y el documento del proyecto de ambos subgrupos del proyecto.
- **README.md:** resumen introductorio sobre la aplicación, de cara a desarrolladores o usuarios que accedan a través del código fuente.

#### Archivos de la aplicación
En este componente tendríamos el archivo `requirements.txt` y las carpetas `scripts`, `app`, `core` y `migrations`.

- **requirements.txt:** lista de dependencias de Python necesarias para el proyecto, instalada mediante `pip`.
- **scripts:** contiene *scripts* varios para automatizar tareas, tales como instalación de dependencias o despliegue.
- **app:** contiene el código principal de la aplicación, destacando principalmente los módulos, los cuales contienen las funcionalidades principales de la aplicación.
- **core:** contiene componentes esenciales usados a lo largo de la aplicación, tales como códigos de utilidad y configuraciones globales.
- **migrations:** contiene los ficheros de migraciones del esquema de la base de datos.

#### Entorno de trabajo
En este componente tendríamos la carpeta `docker`, la carpeta `vagrant` y los archivo `.env.*`.

- **docker:** contiene los componentes necesarios para lanzar la aplicación en Docker, desde archivos de configuración a las imágenes de Docker, por *scripts* para certificados SSL o configuraciones del servidor web NGINX.
- **vagrant:** contiene los componentes necesarios para lanzar la aplicación en Vagrant, es decir el Vagrantfile y los playbooks .yml para que Ansible automatize y gestione la configuración del sistema para Vagrant.
- **.env.*:** incluyen variables de entorno para la aplicación. Los archivos `.env.<deployment_environment>.example` son ejemplos de variables de entorno para ciertos entornos de despliegue.

#### Rosemary CLI
En este componente tendríamos la carpeta `rosemary` y el archivo `setup.py`.

- **rosemary:** contiene el código para el paquete `Rosemary CLI`, el cual está aún en desarrollo. Rosemary es una interfaz de la línea de comandos (*Command Line Interface* - CLI) que tiene el propósito de facilitar la gestión de proyectos y tareas de desarrollo.
- **setup.py:** un `setup.py` es un *script* para distribución de paquetes Python; define propiedades como el nombre, la versión y las dependencias. En este caso se usa para el paquete `Rosemary CLI`.

#### Archivos de configuración
En este componente tendríamos únicamente el archivo .`flake8`.

- **.flake8:** contiene configuraciones para Flake8, la cual es una herramienta de análisis estático de código para Python.

### 4. Peticiones HTTP

![HTTP request UVLHub](https://imgur.com/HCEdGz7.png)

UVLHub siguen una patrón Modelo-Vista-Controlador (MVC) mediante Flask para gestionar las peticiones HTTP. El flujo de información es el siguiente:

- Las peticiones llegan desde internet, donde UVLHub es accesible.
- El servidor Flask recibe las peticiones y las redirige a las rutas.
- Las rutas pueden llamar a los servicios para realizar la lógica de negocio.
- Los servicios interactúan con los repositorios para acceder a los datos de la base de datos según los modelos.
- Los formularios y las plantillas de frontend se usan para manejar los *inputs* de los usuarios y generarles la respuesta necesaria.

### 5. Añadidos al proyecto

En esta sección se enumerarán los cambios desarrollados para el proyecto desde la perspectiva funcional y arquitectónica. Se analizarán los cambios hechos por cada subgrupo para sus work items (WI) y otros cambios adicionales generales.

#### Cambios por el grupo Jamon-Hub-1 para sus WI:

 - **Sign-up validation:** para este WI, se ha incorporado en el módulo `auth` la creación de códigos One-Time Password (OTP) y el uso de un servicio externo de emails para que le lleguen a los usuarios que están realizando el proceso de registro y se pueda validar la veracidad de su registro.
 - **Multiple login:** para este WI, se ha extendido el módulo `auth` para permitir el inicio de sesión a UVLHub con cuentas de ORCID, GitHub y Google. De este modo, se ha integrado la compatibilidad con las APIs de dichas organizaciones enfocadas exclusivamente al inicio de sesión.

 - **Rate datasets/models:** para este WI, se han añadido opciones para valorar modelos y *datasets* mediante estrellas. Se han implementado los cambios tanto en el módulo `models`, como en `datasets`y en `explore`, para poder visualizar las valoraciones.
 - **Download all datasets:** para este WI, se pulió la opción de descargar todos los *datasets*, del módulo `datasets`.

 - **AI integration:** para este WI, se ha añadido un módulo completamente nuevo, `chabot`, el cual implementa el chatbot, realizando la conexión con la API de OpenAI.
 - **Advanced search:** para este WI, se extendió el sistema de búsqueda extendida añadiendo filtros adicionales predefinidos. Los cambios se aplicaron principalmente al módulo `explore`.

#### Cambios por el grupo Jamon-Hub-2, para sus WI:

 - **Remember my password:** para este WI, se ha integrado la funcionalidad para que el sistema reestablezca la contraseña de los usuarios en caso de olvido u otra necesidad. Se ha añdido la creación de códigos One-Time Password (OTP) y se ha usado la funcionalidad de enviar correos electrónicos implementada para sign-up validation. Los cambios se han aplicado a lo largo de todo el módulo `auth`.
 - **Register developer:** para este WI, se ha añadido la opción para que los usuarios se registren como desarrolladores. En el módulo `auth` se ha implementado el registro como usuario, mientras que en los módulos `datasets`y en `profile`se han añadido detalles para reflejar el rol de desarrollador.

 - **Improve UI:** para este WI, se ha realizado un rediseño y optimización de la interfaz gráfica de usuario para mejorar la experiencia del usuario, acercándose al principio de predictabilidad del usuario. El cambio en cuestión se ha implementado en la visualización de los datasets, modificando sus plantillas de frontend, en el módulo `datasets`.
 - **Different versions of models**: para este WI, se ha dado soporte para la conversión directa de los modelos UVL en *datasets* a diferentes formatos. También se han actualizado los *datasets* en el seeder para que también sea aplicables a ellos. Los cambios se han realizado en los módulo `datasets` y `hubfile`.

 - **Staging Area:**  para este WI se ha implementado de un espacio temporal que permite a los usuarios almacenar datasets antes de ser subidos a Zenodo. Se han aplicado cambios en las rutas de `datasets` pero también en frontend, para poder discernir los *datasets* en el nuevo estado. También se han añadido cambios al módulo `hubfile` para poder eliminar dichos *datasets*.
 - **Search Queries:** para este WI, se ha mejorado el sistema de búsqueda para permitir a los usuarios realizar consultas de filtrado específicas y descargar modelos según criterios personalizados. Se ha mejorado las rutas de `dataset` para un mejor filtrado y se ha actualizado el módulo `explore`para incluir las funcionalidades en la búsqueda.

#### Cambios generales:

- **fakenodo:** para este WI, ambos grupos han trabajado en desarrollar un stub que simula la funcionalidad de la API de Zenodo. Se ha creado un módulo enteramente nuevo llamado `fakenodo`, en el que se ha implementado Fakenodo, de forma prácticamente análoga al módulo `zenodo`. También se han reemplazado las llamadas y menciones del módulo `datasets` al módulo `zenodo` por unas al módulo `fakenodo`.

- **workflows:** el *workflow* del *lint* ha sido eliminado, los de *commits* y *tests* han sido mejorado para comprobar nuevos aspectos, y se ha creado uno nuevo para el análisis de la calidad del código mediante Codacy.
- **.env:** se han necesitado nuevas variables de entorno por lo que los desarrolladores han actualizado su archivo `.env`.
- **vagrant:** se han aplicado algunas mejoras para prevenir cambios innecesarios en contraseñas y simplificar la configuración, y también cambiar la variable de entorno para hacerla compatible con Flask Run.
- **documentation:** se ha creado una nueva carpeta que contiene el acta fundacional, el diario del equipo y el documento del proyecto de ambos subgrupos del proyecto.

## Visión Global del Proceso de Desarrollo

En el desarrollo de software, es esencial seguir un proceso claro y bien definido que permita la evolución controlada del producto, garantizando la calidad y la satisfacción del cliente. Este proceso abarca desde la fase de planificación hasta la puesta en producción de los cambios, pasando por el desarrollo, pruebas y gestión de la configuración. A lo largo del ciclo de vida del proyecto, se utilizan diversas herramientas para facilitar la gestión de código, la integración continua, la automatización de pruebas y la comunicación entre los equipos de trabajo.

### 1. Introducción

El proceso de desarrollo de este proyecto se organiza de manera ágil, dividido en *milestones* que funcionan como *sprints*, con una duración aproximada de un mes. Cada *milestone* es un conjunto de tareas y objetivos que el equipo debe cumplir en ese periodo. Durante cada sprint, se seleccionan y priorizan los *Work Items* (WI), que representan funcionalidades o tareas específicas del proyecto. Este enfoque permite mantener un ciclo de trabajo iterativo y flexible, con el fin de adaptar el producto a los requisitos cambiantes y mejorar continuamente la calidad y el rendimiento del sistema. Además, se hace uso de herramientas como GitHub y GitHub Projects para la gestión de las tareas, el seguimiento del progreso y la colaboración entre los miembros del equipo.

### 2. Fases del proceso de desarrollo

El proceso de desarrollo está dividido en varias fases interrelacionadas, cada una con su propio conjunto de tareas y herramientas que facilitan la evolución controlada del producto.

#### Fase de planificación

La planificación es clave en este proceso, ya que establece el alcance y los requisitos de cada *Work Item* (WI). Los WI se desglosan en tareas específicas, y se priorizan según lo acordado en el acta fundacional del proyecto. Cada tarea se asigna a un miembro del equipo y se registra como *issue* en GitHub. Esta fase también contempla la colaboración entre los grupos, la identificación de posibles conflictos o solapamientos entre las tareas de los distintos equipos, y la definición de los tests que deberán cubrir las tareas.

- **Herramientas utilizadas:** GitHub (para registrar *issues* y gestionar proyectos con GitHub Projects).

**Ejemplo:**
Durante la fase de planificación, el equipo selecciona los WI que se trabajarán en el sprint y los desglosa en tareas más pequeñas y manejables. Estas tareas se priorizan con base en los objetivos del proyecto y se etiquetan según su importancia. Además, se asignan a los miembros del equipo, quienes serán responsables de llevarlas a cabo dentro del plazo establecido. Todo este proceso se gestiona a través de GitHub, donde se vinculan los *issues* con los WI correspondientes, y se organiza el trabajo en los proyectos de GitHub (GitHub Projects), tanto para el grupo 1 como para el grupo 2.

#### Fase de diseño

El diseño se lleva a cabo de manera colaborativa, en paralelo a la planificación. Se crean los primeros prototipos visuales de la aplicación, se identifican los módulos a modificar y se definen los tests necesarios. Esta fase también incluye la supervisión para identificar solapamientos entre los WI de los dos grupos, garantizando que no haya conflictos durante el desarrollo.

- **Herramientas utilizadas:** Herramientas de diseño colaborativo (por ejemplo, Draw.io o Sketch), y también GitHub para el seguimiento de posibles solapamientos.

**Ejemplo:**
En la fase de diseño, el equipo trabaja de manera colaborativa para crear los prototipos visuales y la arquitectura de la aplicación. También se identifican los módulos a modificar y se definen las pruebas necesarias para cubrir las tareas del sprint. Además, se asegura de que no haya conflictos con los WI de otros grupos, lo que se gestiona en GitHub a través de la organización de las tareas y su vinculación con los proyectos correspondientes.

#### Fase de desarrollo

En esta fase, cada miembro del equipo trabaja de manera individual sobre las tareas asignadas. La actualización del estado de cada tarea se realiza a través de GitHub Projects. Se fomenta el uso de commits atómicos y el uso de *pull requests* (PR) para actualizar la rama principal, siguiendo las pautas establecidas en el acta fundacional. Antes de comenzar la fase, se crean las *ramas* acorde con lo definido en el acta fundacional. 

- **Herramientas utilizadas:** GitHub (para commits, *pull requests* y seguimiento del progreso a través de GitHub Projects).

**Ejemplo:**
Durante el desarrollo, cada miembro del equipo trabaja en sus tareas asignadas, realizando commits atómicos y utilizando ramas específicas para cada *task* o *incidence*. La actualización de las tareas se realiza en GitHub Projects, donde se registra el progreso de cada tarea. Además, se generan *pull requests* para actualizar la rama principal (`main`), las cuales son revisadas y aprobadas por otros miembros del equipo según las condiciones establecidas en el acta fundacional.

#### Fase de pruebas

Los encargados de realizar las pruebas se encargan de verificar que el WI esté completado y funcione correctamente, comenzando con pruebas unitarias. Dependiendo de la complejidad del WI, se pueden realizar también pruebas de integración, interfaz (con Selenium) y carga (con Locust). La cantidad y el tipo de pruebas se adaptan a las necesidades del WI, y se fomenta la utilización de diversas técnicas de testeo. Frecuentemente, los encargados de testear una característica no son los desarrolladores de dicha tarea. Esto se hace para crear una dinámica de revisión continua.

- **Herramientas utilizadas:** Selenium (para pruebas de interfaz), Locust (para pruebas de carga), etc.

**Ejemplo:**
En la fase de pruebas, los encargados de testing verifican que todas las funcionalidades implementadas cumplan con los requisitos establecidos. Se realizan pruebas unitarias, y en función de la complejidad de cada WI, también se llevan a cabo pruebas de integración y de carga. Las pruebas de interfaz se realizan con Selenium, mientras que las pruebas de carga se llevan a cabo con Locust. Se fomenta la adopción de técnicas de testeo avanzadas, como el testeo de valores límite y el *pairwise*, cuando es necesario.

#### Fase de despliegue

El despliegue se realiza automáticamente utilizando Render cada vez que hay un *push* a la rama principal. Las *pull requests* a main son aceptadas cuando se cumplen las condiciones definidas en el acta fundacional, y el sistema se actualiza automáticamente en el entorno de producción.

- **Herramientas utilizadas:** Render (para despliegue automático).

**Ejemplo:**
El proceso de despliegue es completamente automatizado mediante Render. Cada vez que se hace un *push* a la rama principal (`main`), el sistema se actualiza automáticamente en producción. Las *pull requests* se revisan y aceptan solo cuando cumplen con los requisitos establecidos en el acta fundacional, lo que garantiza que las actualizaciones sean seguras y estables.

#### Fase de mantenimiento

Una vez el sistema está en producción, se realiza un seguimiento continuo de los WI completados. Si se detectan incidencias o mejoras, se registran como *issues* en GitHub, siguiendo el protocolo definido en el acta fundacional.

- **Herramientas utilizadas:** GitHub (para la gestión de incidencias y mejoras).

**Ejemplo:**
En la fase de mantenimiento, el equipo realiza un seguimiento de las tareas ya completadas. Si surge una incidencia, se registra como *issue* en GitHub siguiendo el protocolo establecido. También se registran posibles mejoras o nuevas funcionalidades que se consideran para los siguientes sprints.

### 3. Ejercicio de cambio propuesto

**Cambio propuesto:** Añadir una API que devuelva una imagen aleatoria de un gato cada vez que se suba un nuevo dataset a la aplicación.

#### Descripción del cambio

Este cambio tiene como objetivo mejorar la interacción del usuario con la aplicación al proporcionar una imagen aleatoria de un gato cada vez que se sube un nuevo dataset. Este cambio es simple, pero ilustrativo del proceso de evolución del proyecto. A continuación, se detallan los pasos para implementar este cambio.

#### Proceso para implementar el cambio

**1. Planificación**

- **Requisitos:**
  - Cada vez que un usuario suba un nuevo dataset a la aplicación, se debe llamar a una API externa que proporcione una imagen aleatoria de un gato.
  - La imagen de gato debe mostrarse junto al dataset recién subido en la interfaz de usuario.

- **Tareas:**
  - Integrar la API de gatos en el backend.
  - Modificar el frontend para que pueda recibir y mostrar la imagen del gato junto con el dataset.
  - Verificar que la integración funcione correctamente mediante pruebas.

- **Acciones a realizar:**
  - Se crea la issue correspondiente por cada tarea definida en la planificación y acorde a lo definido en el acta fundacional.

**2. Desarrollo**

- **Acciones a realizar:**
  - Se crea la rama correspondiente acorde a lo definido en el acta fundacional.
  - Se creará una nueva función en el backend que haga la solicitud a la API de gatos.
  - El frontend se actualizará para mostrar la imagen de gato junto con el dataset.

- **Asignación de tareas:**
  - Un miembro del equipo se encargará de la integración de la API.
  - Otro miembro actualizará la interfaz de usuario para mostrar la imagen.

**3. Pruebas**

- **Pruebas necesarias:**
  - Pruebas unitarias para verificar que la API de gatos devuelve correctamente la imagen.
  - Pruebas de interfaz para asegurar que la imagen se muestra correctamente en el frontend después de subir el dataset.
  - Pruebas de carga para comprobar que la API funciona correctamente con un gran volumen de solicitudes.

**4. Despliegue**

El cambio se desplegará automáticamente a través de Render, utilizando el proceso de despliegue automatizado cada vez que se haga un *push* a la rama principal.

**5. Mantenimiento**

Una vez en producción, se hará un seguimiento para asegurar que la integración con la API de gatos funciona correctamente. Si hay incidencias, se registrarán como *issues* en GitHub y se gestionarán en los siguientes sprints.

## Entorno de Desarrollo

En esta sección se detallan los entornos de desarrollo utilizados, las versiones de las herramientas empleadas, y los pasos necesarios para instalar tanto el sistema principal como los subsistemas relacionados para garantizar que el sistema funcione correctamente. Se ofrecen tres métodos de instalación: **Manual**, **Docker** y **Vagrant**. 

#### Entorno de Desarrollo Utilizado

Todos los miembros del equipo han utilizado **Visual Studio Code** como el principal editor de código debido a su flexibilidad y amplia gama de extensiones. Algunos miembros también han utilizado extensiones adicionales para mejorar el flujo de trabajo y la calidad del código:

- **Conventional Commits**: Esta extensión fue utilizada en un primer momento para ayudar a los miembros del equipo a seguir una convención estándar para los mensajes de los commits, antes de contar con un **hook** más personalizado para el proyecto.
- **Flake8**: Para asegurar la calidad del código, se utilizó la extensión Flake8, que realiza un análisis estático del código y ayuda a detectar problemas de estilo y posibles errores de código.

Las versiones de las herramientas y dependencias clave utilizadas en el proyecto se pueden encontrar en el archivo `requirements.txt`.

#### Métodos de Instalación

Solo podemos garantizar la completa compatibilidad del proyecto en sistemas **Linux**. Sin embargo, los usuarios de otros sistemas operativos (como Windows o macOS) son libres de intentar los métodos de instalación detallados a continuación, aunque no podemos asegurar que funcione sin problemas.
A continuación, se detallan los tres métodos de instalación disponibles:

---

### 1. **Instalación Manual**

> **Aviso**: Las instrucciones de instalación que siguen han sido obtenidas de la página [de la documentación oficial del proyecto clonado](https://docs.uvlhub.io/installation).

1. **Clonar el Repositorio**:
   - Clona el repositorio del proyecto:
     ```bash
     git clone https://github.com/davidgonmar/uvlhub-egc.git
     cd uvlhub-egc
     ```

2. **Instalar MariaDB**:
   - MariaDB es una base de datos relacional que necesitamos para nuestra aplicación.
   - Para instalar el paquete oficial de MariaDB en Ubuntu, ejecuta el siguiente comando:
     ```bash
     sudo apt install mariadb-server -y
     ```

3. **Iniciar el servicio de MariaDB**:
   - Una vez instalado, inicia el servicio de MariaDB con el siguiente comando:
     ```bash
     sudo systemctl start mariadb
     ```

4. **Configurar MariaDB**:
   - Ejecuta el script de seguridad para realizar configuraciones iniciales:
     ```bash
     sudo mysql_secure_installation
     ```
   - Sigue estos pasos para configurar correctamente la instalación:
     - **Enter current password for root (enter for none):** (presiona Enter)
     - **Switch to unix_socket authentication [Y/n]:** `y`
     - **Change the root password? [Y/n]:** `y`
       - Nueva contraseña: `uvlhubdb_root_password`
       - Reingresar nueva contraseña: `uvlhubdb_root_password`
     - **Remove anonymous users? [Y/n]:** `y`
     - **Disallow root login remotely? [Y/n]:** `y`
     - **Remove test database and access to it? [Y/n]:** `y`
     - **Reload privilege tables now? [Y/n]:** `y`

5. **Configurar bases de datos y usuarios**:
   - Abre la consola de MariaDB con:
     ```bash
     sudo mysql -u root -p
     ```
   - Usa la contraseña `uvlhubdb_root_password` como la contraseña de root. Luego, ejecuta los siguientes comandos para crear las bases de datos y los usuarios:
     ```bash
     CREATE DATABASE uvlhubdb;
     CREATE DATABASE uvlhubdb_test;
     CREATE USER 'uvlhubdb_user'@'localhost' IDENTIFIED BY 'uvlhubdb_password';
     GRANT ALL PRIVILEGES ON uvlhubdb.* TO 'uvlhubdb_user'@'localhost';
     GRANT ALL PRIVILEGES ON uvlhubdb_test.* TO 'uvlhubdb_user'@'localhost';
     FLUSH PRIVILEGES;
     EXIT;
     ```

6. **Configurar el entorno de la aplicación**:
   - Crea un archivo `.env` con las variables de entorno necesarias o usa la plantilla proporcionada:
     ```bash
     cp .env.local.example .env
     ```
   - Para evitar que el módulo webhook cause problemas en el entorno de desarrollo, ignóralo añadiéndolo al archivo `.moduleignore`:
     ```bash
     echo "webhook" > .moduleignore
     ```

7. **Instalar dependencias**:
   - **Crear y activar un entorno virtual**:
     Si no lo has hecho aún, instala el entorno virtual con:
     ```bash
     sudo apt install python3.12-venv
     python3.12 -m venv venv
     source venv/bin/activate
     ```
   - **Instalar dependencias de Python**:
     Para instalar las dependencias necesarias, ejecuta:
     ```bash
     pip install --upgrade pip
     pip install -r requirements.txt
     ```
   - **Instalar Rosemary en modo editable**:
     Rosemary es una herramienta de línea de comandos que debe ser instalada en modo editable para detectar cambios en tiempo real:
     ```bash
     pip install -e ./
     ```
     Para verificar que la instalación fue correcta, ejecuta:
     ```bash
     rosemary
     ```

8. **Ejecutar la aplicación**:
   - **Aplicar migraciones**:
     Una vez configurado todo, aplica las migraciones para crear las tablas necesarias en la base de datos:
     ```bash
     flask db upgrade
     ```
   - **Poblar la base de datos**:
     Genera datos de prueba para facilitar el uso del sistema sin necesidad de crear las entidades manualmente:
     ```bash
     rosemary db:seed
     ```
   - **Ejecutar el servidor de desarrollo de Flask**:
     Inicia la aplicación con el servidor de desarrollo de Flask. El servidor se ejecutará en el puerto 5000 por defecto:
     ```bash
     flask run --host=0.0.0.0 --reload --debug
     ```

Siguiendo estos pasos, deberías tener el sistema completamente configurado y funcionando en tu entorno local.

---

### 2. **Instalación con Docker**

> **Aviso**: Las instrucciones de instalación que siguen han sido obtenidas de la página [de la documentación oficial del proyecto clonado](https://docs.uvlhub.io/installation).

1. **Instalar Docker**:
   - Asegúrate de tener **Docker** instalado en tu máquina. Si no lo tienes, puedes seguir las instrucciones de instalación en [Docker Docs](https://docs.docker.com/get-docker/).

2. **Copiar el archivo de configuración de entorno**:
   - Primero, copia el archivo `.env.docker.example` al archivo `.env` que se utilizará para establecer las variables de entorno.
     ```bash
     cp .env.docker.example .env
     ```

3. **Iniciar los contenedores**:
   - Para iniciar los contenedores en modo desarrollo, utiliza el archivo `docker-compose.dev.yml` ubicado en el directorio `docker`. El comando se ejecutará en segundo plano (-d).
     ```bash
     docker compose -f docker/docker-compose.dev.yml up -d
     ```

4. **Verificar los contenedores en ejecución**:
   - Para verificar que los contenedores se están ejecutando correctamente, usa el siguiente comando:
     ```bash
     docker ps
     ```
   - Si todo ha funcionado correctamente, deberías poder acceder a la versión desplegada de **uvlhub** en desarrollo en [http://localhost](http://localhost).

5. **Detener los contenedores**:
   - Para detener los contenedores, utiliza el mismo archivo `docker-compose.dev.yml` con el siguiente comando:
     ```bash
     docker compose -f docker/docker-compose.dev.yml down
     ```

6. **Detener los contenedores y eliminar volúmenes**:
   - El comando anterior detiene los contenedores, pero no elimina los volúmenes, lo cual puede ser problemático con **MariaDB** si necesitas cargar una configuración diferente.
   - Para detener los contenedores y eliminar también los volúmenes, utiliza el siguiente comando con el flag `-v`:
     ```bash
     docker compose -f docker/docker-compose.dev.yml down -v
     ```

7. **Recargar la configuración**:
   - Si algún archivo `Dockerfile` o `docker-compose.*.yml` ha sido modificado, es necesario reconstruir las imágenes utilizando el flag `--build`. Para hacerlo, ejecuta:
     ```bash
     docker compose -f docker/docker-compose.dev.yml up -d --build
     ```

Siguiendo estos pasos, podrás ejecutar la aplicación en un entorno Docker y realizar las operaciones necesarias en el entorno de desarrollo.

---

### 3. **Instalación con Vagrant**

> **Aviso**: Las instrucciones de instalación que siguen han sido obtenidas de la página [de la documentación oficial del proyecto clonado](https://docs.uvlhub.io/installation).

1. **Instalar Vagrant y VirtualBox**:
   - Asegúrate de tener **Vagrant** y **VirtualBox** instalados en tu máquina. Si no los tienes, puedes seguir las instrucciones de instalación en [Vagrant Docs](https://www.vagrantup.com/docs) y [VirtualBox Docs](https://www.virtualbox.org/manual/).

2. **Configurar los archivos de entorno**:
   - Primero, copia el archivo `.env.vagrant.example` al archivo `.env` que se utilizará para establecer las variables de entorno.
     ```bash
     cp .env.vagrant.example .env
     ```

3. **Acceder a la carpeta de Vagrant**:
   - Todos los comandos de Vagrant deben ejecutarse dentro de la carpeta `vagrant`, que se encuentra en la raíz del proyecto.
     ```bash
     cd vagrant
     ```

4. **Iniciar la máquina virtual**:
   - Para iniciar la máquina virtual en modo desarrollo, utiliza el archivo `Vagrantfile` ubicado en la carpeta `vagrant`. El comando configurará y ejecutará la VM.
     ```bash
     vagrant up
     ```
   - Si todo ha funcionado correctamente, deberías poder acceder a la versión desplegada de **uvlhub** en desarrollo en [http://localhost:5000](http://localhost:5000).

5. **Acceder a la máquina virtual**:
   - Para acceder a la máquina virtual y ejecutar operaciones desde dentro (como Rosemary), usa el siguiente comando:
     ```bash
     vagrant ssh
     ```
   - Esto te llevará a la consola interna de la máquina virtual. Para salir, simplemente ejecuta:
     ```bash
     exit
     ```

6. **Provisionar la máquina virtual**:
   - Si necesitas volver a ejecutar los scripts de aprovisionamiento (por ejemplo, después de realizar cambios), utiliza uno de los siguientes comandos:
     - Si la máquina virtual está apagada:
       ```bash
       vagrant up --provision
       ```
     - Si la máquina necesita reiniciarse:
       ```bash
       vagrant reload --provision
       ```

7. **Verificar el estado de la máquina virtual**:
   - Para verificar que la máquina virtual esté funcionando correctamente, utiliza el siguiente comando:
     ```bash
     vagrant status
     ```

8. **Detener la máquina virtual**:
   - Para detener la máquina virtual, usa el siguiente comando:
     ```bash
     vagrant halt
     ```

9. **Destruir la máquina virtual**:
   - Para destruir la máquina virtual (eliminando todos los datos), usa el siguiente comando:
     ```bash
     vagrant destroy
     ```

Siguiendo estos pasos, deberías poder configurar, ejecutar y gestionar tu máquina virtual con Vagrant de manera eficiente.

## Ejercicio de Propuesta de Cambio

### 1. Planificación

#### 1.1. Requisitos
El cambio propuesto consiste en agregar un mensaje de bienvenida estático a la página principal de la aplicación. Este mensaje debe ser visible cada vez que se acceda a la página principal.

#### 1.2. Crear y Desglosar Tareas

1. **Desglosar tareas**:
   - **Tarea 1**: Modificar el archivo HTML (`base_template.html`) para incluir el mensaje de bienvenida.
   - **Tarea 2**: (Opcional) Estilizar el mensaje de bienvenida con CSS.

2. **Crear las tareas**: 
    - Se crean las tareas correspondientes definidas en el paso anterior, haciendo uso de la plantilla.
    - Asignamos a un responsable, escribimos una descripción, la etiquetamos, asignamos a un proyecto y ponemos una fecha límite, en este caso en forma de milestone. En el proyecto, marcamos su estado como "Todo" y le asignamos una prioridad. En este caso será Baja. 
    
    ![Texto alternativo](https://i.imgur.com/gKrPmeO.png)

### 2. Desarrollo

Antes de comenzar el desarrollo, crearíamos una rama específica para esta tarea. Como solo tenemos una tarea (la segunda es opcional, y en un desarrollo real, se completaría junto con la primera) en este caso solo necesitaríamos una. Siguiendo las convenciones del acta fundacional, la llamaremos: `g2/task_42/welcome_message` durante la duración de la explicación.

```sql
git checkout -b g2/task_42/welcome_message
```

#### 2.1. Modificar el archivo HTML (`base_template.html`)

Lo primero que necesitamos hacer es modificar el archivo `base_template.html` (que se encuentra en la carpeta `app/templates`) para incluir el mensaje de bienvenida.

1. **Edición de `base_template.html`**:
   
   Vamos al archivo `base_template.html` y agregamos el siguiente bloque de HTML para mostrar el mensaje de bienvenida.

   ```html
        <main class="content">
            <div class="container p-0">
                <div id="welcome-message" class="alert alert-success">
                    <h2>¡Bienvenido a la aplicación!</h2>
                    <p>Estamos felices de tenerte aquí. ¡Disfruta de la experiencia!</p>
                </div>
                {% block content %}{% endblock %}
            </div>
        </main>
    ```

2. **Estilizar el mensaje de bienvenida con CSS**:
  
    Hemos estilizado el mensaje utilizando la clase `alert alert-success` (y por simplicidad en este tutorial, omitiremos el CSS personalizado). El resultado ya es visualmente aceptable.

### 3. Pruebas

#### 3.1. Pruebas manuales

Dado que el cambio es sencillo y no requiere lógica compleja (y por simplicidad en este tutorial), el encargado haría una verificación manual de su funcionamiento. Para ello, seguiría los siguientes pasos de forma aproximada:

1. **Acceso a la página principal de la aplicación**.
   - Asegúrate de estar viendo la página que ha sido modificada.
   
2. **Verificación de que el mensaje de bienvenida se muestra correctamente**.
   - El mensaje debe ser visible en la parte superior de la página principal.
   - El texto debe ser "¡Bienvenido a la aplicación!" seguido de "Estamos felices de tenerte aquí. ¡Disfruta de la experiencia!".

3. **Verificación de que el estilo del mensaje es el adecuado**.
   - El fondo del mensaje debe ser verde claro.

Si todo se muestra correctamente, el cambio ha sido implementado correctamente.

### 4. Creación de la Pull Request

#### 4.1. Hacer commit de los cambios

Una vez que se haya realizado todos los cambios y verificado que todo está funcionando, es el momento de hacer commit de los archivos modificados y hacer push al repositorio.

1. En la terminal, dentro del directorio del proyecto, se ejecutarían los siguientes comandos:
    ```sql
    git add . 
    git commit -m "feat: add welcome message
                  Agregado un mensaje de bienvenida estático en la página principal. 
                  #42"
    git push origin g2/task_42/welcome_message
    ```

#### 4.2. Crear la Pull Request (PR)

1. Se iría a la página del repositorio en GitHub y seleccionaría la opción **Pull Requests**.
2. Clic en **New Pull Request**.
3. Se aseguraría de que la base de la pull request esté en la rama `main` y de que esté comparando la rama de trabajo con esta base.
4. Se escribiría una descripción breve para la PR, como: "Se ha agregado un mensaje de bienvenida estático en la página principal". También incluiríamos "Closes #42" para que la tarea (issue) se cierre automáticamente una vez se apruebe.
5. Clic en **Create Pull Request** y esperaríamos a que fuese revisado y aprobado por otro miembro del equipo. Nosotros, como encargados de la tarea, designamos a este revisor.

### 5. Despliegue

Los cambios se reflejarán automáticamente en el entorno de producción después de que la Pull Request sea aceptada y fusionada con la rama `main`.

### 6. Mantenimiento

Este cambio es muy simple, por lo que el mantenimiento consiste en asegurarse de que el mensaje de bienvenida siga funcionando correctamente. Si más adelante se decide modificar el mensaje, el estilo o cualquier aspecto relacionado, se puede editar directamente el archivo `base_html.html`. Todo esto tendría que gestionarse a través de una incidencia. El proceso es similar a este, pero con otras plantillas de issues y ramas.


## Conclusiones y Trabajo Futuro

Se enunciarán algunas conclusiones y se presentará un apartado sobre las mejoras que se proponen para el futuro (curso siguiente) y que no han sido desarrolladas en el sistema que se entrega.