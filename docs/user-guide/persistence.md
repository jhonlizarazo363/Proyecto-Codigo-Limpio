# Persistencia de Datos

El sistema utiliza archivos **JSON** para almacenar la información.

---

# Estructura de datos

```json
[
  {
    "id": 1,
    "name": "Juan",
    "email": "juan@email.com"
  }
]
```

---

# Funcionamiento

* Los datos se guardan en archivos JSON
* Se convierten desde objetos Python (dataclasses)
* Se cargan al iniciar el sistema

---

# Ventajas

* Fácil de implementar
* Legible
* No requiere base de datos externa

---


