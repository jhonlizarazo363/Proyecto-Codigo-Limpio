# Sistema de Alquiler de Vehículos

# Descripción

Este proyecto implementa un sistema de gestión de alquiler de vehículos mediante una **interfaz de línea de comandos (CLI)**. Permite registrar clientes, vehículos y gestionar alquileres de forma sencilla.

El sistema fue desarrollado aplicando principios de **código limpio**, separación de responsabilidades y buenas prácticas en Python.

---

# Características principales

* Registro de clientes y vehículos
* Gestión de alquileres
* Persistencia de datos en archivos JSON
* Validaciones en modelos
* Arquitectura modular por capas

---

# Arquitectura del sistema

El sistema está dividido en tres capas principales:

* **CLI** → Interacción con el usuario
* **Servicios** → Lógica del negocio
* **Storage** → Manejo de datos

mermaid
flowchart LR
CLI --> Service
Service --> Storage
Storage --> JSON


---

# Objetivo del proyecto

Aplicar buenas prácticas de desarrollo como:

* Código limpio
* Uso de dataclasses
* Validaciones automáticas
* Separación de capas

