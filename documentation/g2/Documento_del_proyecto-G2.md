# Documento del proyecto

El presente documento tiene como objetivo sintetizar los aspectos clave del proyecto elegido para su desarrollo, en relación con los temas abordados durante las clases. En él, se identifican claramente los miembros del equipo, los grupos a los que pertenecen, el curso académico, y el nombre del proyecto, siguiendo la política de nomenclatura establecida. 

## Indicadores del proyecto

| Miembro del equipo                             | Horas | Commits | LoC  | Test | Issues | Work Item         |
|------------------------------------------------|-------|---------|------|------|--------|-------------------|
| [Barrera Garrancho, María del Carmen](https://github.com/Playeira01) | HH    | XX      | YY   | ZZ   | II     | Descripción breve |
| [García Martínez, Carlos](https://github.com/Cargarmar18)            | HH    | XX      | YY   | ZZ   | II     | Descripción breve |
| [García Sebastián, Javier](https://github.com/JaviGarcia1)           | HH    | XX      | YY   | ZZ   | II     | Descripción breve |
| [Meana Iturri, Claudia](https://github.com/clameaitu)               | HH    | XX      | YY   | ZZ   | II     | Descripción breve |
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
    - Enlace para revisar los **resultados de test en GitHub Actions**: [GitHub Actions Tests](https://github.com/davidgonmar/uvlhub-egc/actions/workflows/ tests.yml)
- **Issues gestionadas**:
  - Enlace: [Issues en GitHub](https://github.com/davidgonmar/uvlhub-egc/issues)
    - Se puede filtrar por etiquetas, autor o estado de la issue (abierta/cerrada) para ver la gestión de las tareas e incidencias.
- **Work Items**:
  - Los work items del proyecto se asocian con las **Issues** en GitHub. Aunque cada miembro del equipo ha dedicado más tiempo a ciertos WI que a otros, todos han participado activamente en diversas tareas relacionadas con diferentes WI. Este enfoque busca promover un ambiente colaborativo, favoreciendo la revisión continua y el trabajo en equipo para alcanzar los objetivos del proyecto de manera eficiente.
    - Enlace: [Issues en GitHub](https://github.com/davidgonmar/uvlhub-egc/issues)

## Integración con otros equipos

Equipos con los que se ha integrado y los motivos por los que lo ha hecho y lugar en el que se ha dado la integración:

- **Jamon-Hub-1**: La integración con este equipo se dio para coordinar los solapamientos de funcionalidad en los **Work Items** (WIs) identificados. Los WIs de ambos equipos tenían puntos de intersección que requerían una estrecha colaboración para garantizar una implementación coherente y evitar conflictos en la funcionalidad del proyecto. La integración se dio principalmente en los módulos de autenticación, búsqueda y descarga de datasets, así como en la mejora de la interfaz de usuario. Los puntos clave de solapamiento fueron los siguientes:
  
  - **Advanced Search**  y **Search Queries**: Ambos WIs se enfocaban en la búsqueda y filtrado de modelos, lo que generaba conflictos en la implementación de los criterios de búsqueda.
  
  - **Sign-up Validation**, **Multiple Login**, **Remember My Password**, y **Register Developer**: Estos WIs, relacionados con la autenticación, impactaban en los módulos `auth` y `profile`. La coordinación entre los equipos fue esencial para evitar duplicaciones y asegurar la coherencia en la funcionalidad de autenticación y envío de emails.

  - **Different Versions of Models**, **Search Queries** y **Download All Datasets**: Estos tres WIs estaban interconectados en términos de la descarga y manejo de datasets. *Different Versions of Models* establecía el proceso de conversión a diferentes formatos, *Search Queries* permitía seleccionar modelos específicos, y *Download All Datasets* facilitaba la descarga de todos los formatos. La implementación coordinada de estos WIs fue crucial para asegurar que se reutilizaran las funcionalidades desarrolladas en cada uno.

Esta integración se dio en un esfuerzo por optimizar el flujo de trabajo entre los equipos, mejorar la cohesión del proyecto y garantizar la calidad del producto final.

## Resumen ejecutivo (800 palabras aproximadamente)

Se sintetizará de un vistazo lo hecho en el trabajo y los datos fundamentales. Se usarán palabras para resumir el proyecto presentado. Contendrá, al menos la siguiente información:

## Descripción del sistema (1.500 palabras aproximadamente)

Se explicará el sistema desarrollado desde un punto de vista funcional y arquitectónico. Se hará una descripción tanto funcional como técnica de sus componentes y su relación con el resto de subsistemas. Habrá una sección que enumere explícitamente cuáles son los cambios que se han desarrollado para el proyecto.

## Visión global del proceso de desarrollo (1.500 palabras aproximadamente)

Debe dar una visión general del proceso que ha seguido enlazándolo con las herramientas que ha utilizado. Ponga un ejemplo de un cambio que se proponga al sistema y cómo abordaría todo el ciclo hasta tener ese cambio en producción. Los detalles de cómo hacer el cambio vendrán en el apartado correspondiente.

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

## Ejercicio de propuesta de cambio

Se presentará un ejercicio con una propuesta concreta de cambio en la que a partir de un cambio que se requiera, se expliquen paso por paso (incluyendo comandos y uso de herramientas) lo que hay que hacer para realizar dicho cambio. Debe ser un ejercicio ilustrativo de todo el proceso de evolución y gestión de la configuración del proyecto.

## Conclusiones y trabajo futuro

Se enunciarán algunas conclusiones y se presentará un apartado sobre las mejoras que se proponen para el futuro (curso siguiente) y que no han sido desarrolladas en el sistema que se entrega.