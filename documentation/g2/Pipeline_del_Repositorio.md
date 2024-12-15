# Jamón-Hub - Pipeline del Repositorio

- **Grupo**: G3
- **Nombre del grupo**: jamon-hub-2
- **Tutor**: Jesús Moreno León
- **Curso Escolar**: 2024/2025  
- **Asignatura**: Evolución y Gestión de la Configuración

### Enlaces de interés:

- **Repositorio de código**: [https://github.com/davidgonmar/uvlhub-egc](https://github.com/davidgonmar/uvlhub-egc)  
- **Sistema desplegado**: [https://uvlhub-egc.onrender.com/](https://uvlhub-egc.onrender.com/)

---

## Índice

1. [Estructura del Pipeline](#estructura-del-pipeline)
   - [Tras Pull Request (PR)](#1-tras-pull-request-pr)
   - [Después del Merge](#2-después-del-merge)
   - [Workflows Independientes](#3-workflows-independientes)
2. [Diagrama del Pipeline](#diagrama-del-pipeline)
3. [Hook Locales](#hooks-locales-para-validación)
   - [Hook Local para Validación de Mensajes de Commit](#hook-local-para-validación-de-mensajes-de-commit)
   - [Hook Local para Validación de Código con Flake8](#hook-local-para-validación-de-código-con-flake8)
4. [Beneficios del Pipeline](#beneficios-del-pipeline)

---

El presente documento describe el pipeline del repositorio para la integración y el despliegue continuo (CI/CD) del proyecto.

## Estructura del Pipeline

El pipeline principal está estructurado en 2 fases principales:

1. **Tras Pull Request (PR)**:
   - Validación inicial para asegurar que el código cumple con los estándares antes de proceder con el merge.
2. **Tras hacer Merge**:
   - Solo se activa tras un merge exitoso a la rama principal (`main`). Los merge a esta rama solo tienen lugar si un compañero del equipo ha revisado y aceptado la pull request correspondiente.
También existen dos workflows independientes que se ejecutan manualmente o una vez cada periodo de tiempo.

### **1. Tras Pull Request (PR)**

Cuando se crea o actualiza un Pull Request hacia la rama principal, se ejecutan los siguientes workflows en paralelo:

- **Commit Syntax Checker**:
  - Verifica que los mensajes de los commits sigan el estándar de convenciones establecido.
  - Workflow: `commits.yml`

- **Run Tests with Coverage**:
  - Ejecuta las pruebas del proyecto y genera un reporte de cobertura.
  - Workflow: `test.yml`

- **Codacy CI**:
  - Analiza la calidad del código usando Codacy para asegurar que no se introduzcan problemas técnicos o de estilo.
  - Workflow: `codacy.yml`
 
- **Dependency Graph and Usage Report**:
  - Este workflow genera un gráfico de dependencias del proyecto y un informe de uso de dependencias en el código y sube ambos como artefactos.
  - Workflow: `dependency_report.yml`
 
Otro añadido al proyecto es el bot **CodiumAI PR-Agent**, este bot se encarga de realizar una extensa y detallada descripción de las pull requests. En su momento se creó un workflow para que este bot también aceptara las pull, requests aunque fue descartado. Ambos grupos estaban de acuerdo en que todas las PRs debían ser revisadas por al menos un compañero humano.

> Aclaración: si sobre una PR activa se realiza un nuevo commit los trabajos se lanzarán nuevamente.

### **2. Después del Merge**

Si todos los workflows de la fase anterior se ejecutan con éxito y un compañero acepta su pull request se realiza un merge hacia `main`, el pipeline continúa con las siguientes tareas:

1. **Despliegue Automático en Render**:
   - Usa el dockerfile para desplegar la aplicación en Render.
   - Para la base de datos se utiliza el servicio de fliess.io.
   - Workflow: `deployment_on_render.yml`
     
2. **Construcción y Publicación de la Imagen Docker**:
   - Se construye la imagen Docker basada en el código del release.
   - Publica la imagen en Docker Hub con el tag correspondiente y un tag `latest`.
   - Workflow: `deployment_on_dockerhub.yml`

### **3. Workflows Independientes**

1. **Historical Contributor Report**:
   - Genera un histórico con todas los contribuciones del repositorio por cada participante.
   - Se ejecuta manualmente y genera un issue a nombre del dueño del repositorio con el informe.
   - Workflow: `historical_report.yml`
     
2. **Monthly Contributor Report**:
   - Genera un histórico con todas los contribuciones del repositorio por cada participante del último mes.
   - Se ejecuta automáticamente cada mes y genera un issue a nombre del dueño del repositorio con el informe.
   - Es posible ejecutarlo manualmente.
   - Workflow: `monthly_report.yml`

## Diagrama del Pipeline

![Pipeline_Jamon drawio](https://github.com/user-attachments/assets/23b17c1a-8039-4f85-b1a6-762d2c8cd5ca)

## Hooks Locales para Validación

Además de las verificaciones en el pipeline CI/CD, el repositorio incluye varios **hooks locales** configurados en el directorio `.git/hooks`. Estos hooks ayudan a garantizar que tanto los mensajes de commit como el código fuente cumplan con los estándares definidos por el equipo antes de que sean enviados al repositorio remoto.

### Hook Local para Validación de Mensajes de Commit

Este hook, ubicado en `.git/hooks/commit-msg`, valida que los mensajes de commit sigan la plantilla establecida antes de permitir que el commit sea agregado.

### Hook Local para Validación de Código con Flake8

Otro hook importante incluido en el repositorio revisa el código fuente antes de que se complete un commit. Este hook se encarga de verificar que el código cumpla con los estándares de estilo definidos por *flake8*. Al validar localmente, el hook evita que errores comunes lleguen al pipeline, donde herramientas como Codacy realizarían validaciones similares.  

#### Configuración de los Hooks

Para que estos hooks funcionen correctamente, los desarrolladores deben copiar el archivo correspondiente al directorio `.git/hooks` en su máquina local. Esto se puede automatizar utilizando herramientas de configuración del entorno o scripts iniciales del proyecto.

---

## Beneficios del Pipeline

- **Automatización**: Reducción de errores humanos mediante tareas automatizadas.
- **Eficiencia**: Validaciones paralelas para reducir tiempos de ejecución.
- **Calidad Garantizada**: Cada paso del pipeline asegura que solo se mergea y despliega código de calidad.
- **Escalabilidad**: La estructura del pipeline es modular y fácil de extender según las necesidades futuras.