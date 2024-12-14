<div align="center">

  <a href="">[![Pytest Testing Suite](https://github.com/davidgonmar/uvlhub-egc/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/davidgonmar/uvlhub-egc/actions/workflows/tests.yml)</a>
  <a href="">[![Commits Syntax Checker](https://github.com/davidgonmar/uvlhub-egc/actions/workflows/commits.yml/badge.svg?branch=main)](https://github.com/davidgonmar/uvlhub-egc/actions/workflows/commits.yml)</a>

</div>

<div align="center">
  <img src="https://www.uvlhub.io/static/img/logos/logo-light.svg" alt="Logo">
</div>

<br>

## 🌍 **Select Language**

**English** | **Español**  
--- | ---  
[English](#uvlhub-clone---egc-project) | [Español](#uvlhub-clon---proyecto-egc)


# UVLHub (Clone) - EGC Project

## 🌟 **About this Project** 

This repository is a **clone** of the original UVLHub project. It contains feature models in **UVL format**, integrated with **Zenodo** and **flamapy**, following the principles of **Open Science**.

This project was developed as part of a **university course** called **EGC** by the group **Jamon-Hub**, composed of **Jamon-Hub-1** and **Jamon-Hub-2**. We aim to enhance the original project by adding new features and to follow the CI/CD principles.

### 🔧 **What does ours include?**  

This project is a clone of **UVLHub**, designed to replicate its main features. However, we didn’t stop there: we’ve added new functionalities and improvements that expand its capabilities, enhance the user experience, and offer fantastic new features.

Our goal is to maintain the essence of the original project while taking it to the next level by implementing features that make it more versatile and up-to-date.

**Jamon-Hub-1** includes the following functionalities:

- **AI integration:** Integration of artificial intelligence into the application. Initially, OpenAI’s AI will be used. Users will be able to request information about UVL models via its API.
- **Advanced search:** An advanced search feature that allows users to filter models based on specific criteria.
- **Download all datasets:** An option that lets users download all available datasets in all formats with a single click.
- **Rate datasets/models:** A function that enables users to rate datasets and models.
- **Sign-up validation:** Email validation process to complete user registration.
- **Multiple login:** An option for users to log in using their ORCID, GitHub, or Google accounts.

**Jamon-Hub-2** will develop the following:  

- **Fakenodo:** Implementation of a stub called "Fakenodo" that replaces the Zenodo API, allowing its functionality to be simulated without relying on an actual external service. Both teams will collaborate on Fakenodo.
- **Staging Area:** Implementation of a temporary space where users can store datasets before uploading them to Zenodo.  
- **Search Queries:** Development of advanced functionalities that allow users to make specific queries to filter and download models according to personalized criteria.  
- **Improve UI:** Redesign and optimization of the graphical user interface to enhance the user experience. The dataset display should resemble GitHub’s layout.  
- **Different versions of models:** Support for multiple model versions and their download in various formats.  
- **Remember my password:**  Integration of a password recovery system that allows users to securely reset their password in case they forget it, ensuring easy access to the application while maintaining account security. 
- **Register developer:** An option for users to register as developers.  

### 🔗 **Original Project** 

- The original UVLHub project is available here: [UVLHub](https://www.uvlhub.io)

- And the original GitHub repository: [Repository](https://github.com/diverso-lab/uvlhub)

## 🚀 **Official Documentation**  

The official documentation of the original project can be found at:  
[docs.uvlhub.io](https://docs.uvlhub.io/)  

All information related to installation, modifications, and contributions to the project can be found in the official documentation.

## 🌐 **Deployed Application**  

You can access the deployed version of the application at the following link:

- **[UVLHub Live](https://uvlhub-egc.onrender.com/)**

This version is hosted and continuously updated to reflect the latest changes made to the project. Feel free to explore the functionality and try out the features!

## 🐳 **Docker Repository**

We provide a **Docker image** for the latest version of the project, making it easy to deploy and run the application. This image contains all necessary dependencies and configurations for running the application seamlessly.

You can access our Docker repository and pull the latest image using the following link:

- **[UVLHub Docker Repository](https://hub.docker.com/repository/docker/cargarmar18/uvlhub-egc/settings)**  

### **Pulling the latest image**

To pull the latest version of the Docker image, run the following command:  
```bash
docker pull cargarmar18/uvlhub-egc:latest
```

# UVLHub (Clon) - Proyecto EGC

## 🌟 **Sobre este Proyecto**

Este repositorio es un **clon** del proyecto original **UVLHub**. Contiene modelos de características en formato **UVL**, integrados con **Zenodo** y **flamapy**, siguiendo los principios de **Ciencia Abierta**.

Este proyecto fue desarrollado como parte de un **curso universitario** llamado **EGC** por el grupo **Jamon-Hub**, compuesto por **Jamon-Hub-1** y **Jamon-Hub-2**. Nuestro objetivo es mejorar el proyecto original añadiendo nuevas características y seguir los principios de **CI/CD**.

### 🔧 **¿Qué incluye el nuestro?** 

Este proyecto es un clon de **UVLHub**, diseñado para replicar sus principales características. Sin embargo, no nos hemos quedado ahí: hemos añadido nuevas funcionalidades y mejoras que amplían sus capacidades, mejora la experiencia de usuario ofreciendo funcionalidades fantásticas.

Nuestro objetivo es mantener la esencia del proyecto original mientras lo llevamos al siguiente nivel con la implementación de features que lo hacen más versátil y actualizado.

Por parte de **Jamon-Hub-1** se incluirá las siguientes funcionalidades:

- **AI integration:** implementación de una inteligencia artificial en la aplicación. En principio se usará una IA de OpenAI. Los usuarios, podrán solicitar, mediante su API, información a la IA sobre  modelos UVL.
- **Advanced search:** funcionalidad de búsqueda avanzada que permitirá a los usuarios filtrar modelos según criterios específicos.
- **Download all datasets:** opción que permitirá a los usuarios descargar todos los _datasets_ disponibles en todos los formatos presionando un solo botón.
- **Rate datasets/models:** función que permitirá a los usuarios para dejar valoraciones a _datasets_ y modelos.
- **Sign-up validation:** proceso de validación del correo electrónico para llevar a cabo el registro de los usuarios.
- **Multiple login:** opción para que los usuarios inicien sesión utilizando sus cuentas de ORCID, GitHub o Google.

Por último **Jamon-Hub-2** desarrollará:

- **Fakenodo:** implementación de un stub denominado "Fakenodo" que reemplazará la API de Zenodo, permitiendo simular su funcionalidad sin depender de un servicio externo real. Ambos equipos trabajarán en Fakenodo.
- **Staging Area**: Implementación de un espacio temporal que permite a los usuarios almacenar datasets antes de ser subidos a Zenodo.  
- **Search Queries**: Desarrollo de funcionalidades avanzadas que permiten a los usuarios realizar consultas específicas para filtrar y descargar modelos según criterios personalizados.
- **Improve UI**: Rediseño y optimización de la interfaz gráfica de usuario para mejorar la experiencia del usuario. La visualización de los datasets debe ser similar a la de GitHub.
- **Different versions of models**: Soporte para diferentes versiones de modelos y su descarga en varios formatos.
- **Remember my password**: Integración de un sistema de recuperación de contraseña que permite a los usuarios restablecer su contraseña de manera segura en caso de olvidarla, garantizando un acceso sencillo a la aplicación sin comprometer la seguridad de la cuenta.
- **Register developer**: Opción para que los usuarios se registren como desarrolladores.

### 🔗 **Proyecto Original**  

- El proyecto original de **UVLHub** está disponible aquí: [UVLHub](https://www.uvlhub.io)

- Y el repositorio original de GitHub: [Repositorio](https://github.com/diverso-lab/uvlhub)

## 🚀 **Documentación Oficial** 
 
La documentación oficial del proyecto original se puede encontrar en:  
[docs.uvlhub.io](https://docs.uvlhub.io/)  

Toda la información relacionada con la instalación, modificaciones y contribuciones al proyecto se puede consultar en la documentación oficial.

## 🌐 **Aplicación Desplegada**  

Puedes acceder a la versión desplegada de la aplicación en el siguiente enlace:

- **[UVLHub en Vivo](https://uvlhub-egc.onrender.com/)**

Esta versión está hospedada y actualizada continuamente para reflejar los últimos cambios realizados en el proyecto. ¡No dudes en explorar la funcionalidad y probar las características!

## 🐳 **Repositorio de Docker**

Proporcionamos una **imagen Docker** con la última versión del proyecto, lo que facilita desplegar y ejecutar la aplicación. Esta imagen contiene todas las dependencias y configuraciones necesarias para ejecutar la aplicación sin problemas.

Puedes acceder a nuestro repositorio de Docker y descargar la última imagen utilizando el siguiente enlace:

- **[Repositorio de Docker de UVLHub](https://hub.docker.com/repository/docker/cargarmar18/uvlhub-egc/settings)**  

### **Descargar la última imagen**

Para descargar la última versión de la imagen Docker, ejecuta el siguiente comando:  
```bash
docker pull cargarmar18/uvlhub-egc:latest
```