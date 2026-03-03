Sistema de Alquiler de Vehículos

1. Descripción del Proyecto

El Sistema de Alquiler de Vehículos es una aplicación de línea de comandos (CLI) desarrollada en Python que permite gestionar el proceso completo de alquiler de vehículos.

El sistema permite:

Registrar vehículos

Registrar clientes

Crear alquileres

Devolver vehículos

Consultar vehículos disponibles

El proyecto fue desarrollado aplicando una arquitectura por capas estricta, separando responsabilidades en:

Models → Definición pura de datos usando @dataclass

Storage → Persistencia en archivo JSON (única capa que puede leer/escribir)

Services → Reglas de negocio y validaciones

CLI → Interfaz de usuario usando Typer + Rich

Tests → Pruebas unitarias con pytest

2. Propósito

El propósito del proyecto es demostrar:

-Separación clara de responsabilidades
-Aplicación de reglas de negocio
-Uso de excepciones personalizadas
-Persistencia en archivos JSON
-Pruebas unitarias robustas
-Buenas prácticas de código (type hinting, docstrings, ruff)

3. Cómo funciona el sistema
* Models

Contiene las dataclasses:

Vehiculo

Cliente

Alquiler

Estas clases solo representan datos.
No contienen lógica de negocio.

* Storage

Encargado exclusivamente de:

Leer el archivo database.json

Escribir en database.json

Convertir objetos ↔ JSON

No valida reglas de negocio.

* Services

Aquí vive la lógica principal:

Reglas implementadas:

 No se puede alquilar si el vehículo no está disponible

 No se puede alquilar si el cliente está inactivo

 No se puede alquilar si el cliente ya tiene un alquiler activo

 No se puede devolver un alquiler ya finalizado

 No se puede operar con IDs inexistentes

* CLI

Interfaz construida con:

Typer → Comandos

Rich → Colores y tablas

Permite interactuar con el sistema desde la terminal.

4. Guía de Instalación

* Requisitos

Python 3.12+
uv instalado

* Paso 1 — Clonar repositorio

git clone <url-del-repositorio>
cd nombre-del-proyecto
Paso 2 — Instalar dependencias
uv sync

Esto crea el entorno virtual automáticamente.

5. Manual de Uso (CLI)

Todos los comandos se ejecutan así:

uv run python main.py <comando>

 -Crear un Vehículo
uv run python main.py crear-vehiculo Toyota Corolla 2020 Rojo ABC123 120

Parámetros:

Marca

Modelo

Año

Color

Placa

Precio por día

Resultado:

Se crea el vehículo como disponible automáticamente.

- Crear un Cliente
uv run python main.py crear-cliente Juan 123456 juan@test.com

El cliente queda activo automáticamente.

- Listar Vehículos

uv run python main.py listar-vehiculos

Muestra una tabla con:

ID

Marca

Modelo

Disponibilidad

- Crear un Alquiler
uv run python main.py alquilar 1 1

Parámetros:

ID del cliente

ID del vehículo

Reglas que se validan:

Cliente debe existir

Vehículo debe existir

Cliente debe estar activo

Vehículo debe estar disponible

Cliente no puede tener otro alquiler activo

Si todo es correcto:

Se crea el alquiler

El vehículo cambia a no disponible

- Devolver un Vehículo

uv run python main.py devolver 1

Parámetro:

ID del alquiler

Al devolver:

El alquiler se marca como inactivo

Se registra la fecha de devolución

El vehículo vuelve a estar disponible

6. Pruebas Unitarias

El proyecto incluye pruebas automáticas con pytest.

Para ejecutarlas:

uv run pytest

Las pruebas cubren:

Creación correcta de vehículos

Creación correcta de clientes

Creación de alquiler válido

Intentos inválidos (errores)

Devoluciones

Reglas de negocio

Excepciones personalizadas

Todas deben pasar correctamente.