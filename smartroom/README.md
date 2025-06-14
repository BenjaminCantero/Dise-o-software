# SmartRoom - Sistema de Gestión de Reservas de Salas

SmartRoom es una solución integral para la gestión inteligente de salas y reservas en instituciones educativas. Incluye una API REST desarrollada con FastAPI y una aplicación de escritorio moderna construida con Tkinter, permitiendo a estudiantes, profesores y administradores gestionar espacios y horarios de manera eficiente y centralizada.

---

## Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecución](#ejecución)
- [API REST](#api-rest)
  - [Endpoints Principales](#endpoints-principales)
  - [Ejemplos de Uso](#ejemplos-de-uso)
- [Aplicación de Escritorio (GUI)](#aplicación-de-escritorio-gui)
- [Modelos y Servicios](#modelos-y-servicios)
- [Patrones de Diseño Utilizados](#patrones-de-diseño-utilizados)
- [Buenas Prácticas y Recomendaciones](#buenas-prácticas-y-recomendaciones)
- [Contribuciones](#contribuciones)
- [Autores](#autores)
- [Licencia](#licencia)

---

## Características

- **Gestión de usuarios:** Alta, baja y modificación de estudiantes, profesores y administradores.
- **Gestión de salas:** Creación, edición y eliminación de salas con control de capacidad y estado.
- **Reservas inteligentes:** Creación de reservas con validación de solapamientos y horarios.
- **Panel de horario:** Visualización clara y filtrada de reservas según usuario y rol.
- **API RESTful:** Backend robusto y documentado con FastAPI.
- **Interfaz gráfica moderna:** Aplicación de escritorio intuitiva y responsiva con Tkinter.
- **Patrones de diseño:** Uso de Singleton, Builder, Observable, Mediator, Command y Factory para una arquitectura escalable y mantenible.
- **Notificaciones y actualizaciones en tiempo real** (dentro de la GUI).
- **Soporte para SQLite** (por defecto) y fácil adaptación a otros motores de base de datos.

---

## Estructura del Proyecto

```
Dise-o-software/
│
├── api/                  # Backend REST con FastAPI y SQLAlchemy
│   ├── db.py
│   ├── main.py
│   ├── models/           # Modelos SQLAlchemy
│   ├── schemas/          # Schemas Pydantic
│   ├── routes/           # Endpoints de la API
│   └── services/         # Lógica de negocio
│
├── smartroom/            # Aplicación de escritorio (Tkinter)
│   ├── main.py
│   ├── gui/              # Paneles y diálogos de la interfaz gráfica
│   ├── builders/         # Builders para objetos complejos
│   ├── commands/         # Comandos para acciones (crear, editar, cancelar)
│   ├── core/             # Clases base y utilidades (Observable, Singleton, etc.)
│   ├── factories/        # Fábricas de diálogos y paneles
│   └── mediator/         # Mediador para comunicación entre componentes
│
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Este archivo
```

---

## Instalación y Configuración

### 1. Clona el repositorio

```sh
git clone <url-del-repo>
cd Dise-o-software
```

### 2. Crea un entorno virtual (opcional pero recomendado)

```sh
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```

### 3. Instala las dependencias

```sh
pip install -r requirements.txt
```

### 4. Configura la base de datos (opcional)

Por defecto, se utiliza SQLite. Si deseas usar otro motor, edita `api/db.py` y ajusta la cadena de conexión.

---

## Ejecución

### 1. Iniciar la API REST

Desde la raíz del proyecto:

```sh
uvicorn api.main:app --reload
```

La API estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 2. Iniciar la aplicación de escritorio

Desde la raíz del proyecto:

```sh
python smartroom/main.py
```

O haciendo doble clic en `smartroom/main.py`.

---

## API REST

### Endpoints Principales

- **Usuarios:**  
  - `GET /usuarios/` - Listar usuarios  
  - `POST /usuarios/` - Crear usuario  
  - `PUT /usuarios/{id}` - Editar usuario  
  - `DELETE /usuarios/{id}` - Eliminar usuario

- **Salas:**  
  - `GET /salas/` - Listar salas  
  - `POST /salas/` - Crear sala  
  - `PUT /salas/{id}` - Editar sala  
  - `DELETE /salas/{id}` - Eliminar sala

- **Reservas:**  
  - `GET /reservas/` - Listar reservas  
  - `POST /reservas/` - Crear reserva  
  - `PUT /reservas/{id}` - Editar reserva  
  - `DELETE /reservas/{id}` - Eliminar reserva

### Ejemplos de Uso

#### Crear una sala

```http
POST /salas/
Content-Type: application/json

{
  "nombre": "Sala 101",
  "capacidad": 30,
  "estado": "disponible"
}
```

#### Crear una reserva

```http
POST /reservas/
Content-Type: application/json

{
  "sala_nombre": "Sala 101",
  "usuario_username": "juanperez",
  "fecha_inicio": "2025-06-14T10:00:00",
  "fecha_fin": "2025-06-14T12:00:00"
}
```

#### Listar reservas

```http
GET /reservas/
```

Respuesta:
```json
[
  {
    "id": 1,
    "sala_nombre": "Sala 101",
    "usuario_username": "juanperez",
    "fecha_inicio": "2025-06-14T10:00:00",
    "fecha_fin": "2025-06-14T12:00:00"
  }
]
```

---

## Aplicación de Escritorio (GUI)

- **Inicio de sesión:** Acceso según rol (estudiante, profesor, admin).
- **Panel de reservas:** Visualiza, crea, edita y elimina reservas.
- **Panel de salas:** Gestión de salas (solo admin).
- **Panel de usuarios:** Gestión de usuarios (solo admin).
- **Panel de horario:** Visualización clara de reservas, filtradas por usuario y rol.
- **Dashboard:** Estadísticas y resumen de uso (solo admin).
- **Diseño moderno:** Uso de colores, iconos y estilos personalizados.

---

## Modelos y Servicios

### Modelos principales (`api/models/`):

- **Usuario:**  
  - `id`: int  
  - `username`: str  
  - `password`: str  
  - `role`: str (admin, profesor, estudiante)

- **Sala:**  
  - `id`: int  
  - `nombre`: str  
  - `capacidad`: int  
  - `estado`: str

- **Reserva:**  
  - `id`: int  
  - `sala_id`: int  
  - `usuario_id`: int  
  - `fecha_inicio`: datetime  
  - `fecha_fin`: datetime

### Servicios (`api/services/`):

- **user_service.py:** Lógica de usuarios (autenticación, CRUD)
- **sala_service.py:** Lógica de salas (CRUD, validaciones)
- **reserva_service.py:** Lógica de reservas (CRUD, validación de solapamientos, filtrado por usuario/rol)

---

## Patrones de Diseño Utilizados

- **Singleton:** Servicios y controladores únicos.
- **Builder:** Creación flexible de objetos complejos (reservas, salas).
- **Observable:** Notificación de cambios entre componentes (actualización de paneles).
- **Mediator:** Comunicación desacoplada entre paneles de la GUI.
- **Command:** Encapsulamiento de acciones (crear, editar, cancelar reservas).
- **Factory:** Creación de diálogos y paneles según contexto.

---

## Buenas Prácticas y Recomendaciones

- **Estructura modular:** Mantén separados los modelos, servicios, rutas y componentes de la GUI.
- **Usa entornos virtuales:** Para evitar conflictos de dependencias.
- **Documenta tu código:** Usa docstrings y comentarios claros.
- **Manejo de errores:** Captura y muestra mensajes claros tanto en la API como en la GUI.
- **Pruebas:** Agrega tests unitarios para los servicios y modelos.
- **Seguridad:** No almacenes contraseñas en texto plano en producción. Usa hashing seguro.
- **Configuración:** Usa variables de entorno para datos sensibles (DB, claves, etc.).

---

## Contribuciones

¡Las contribuciones son bienvenidas!  
Por favor, abre un issue o pull request para sugerencias, mejoras o correcciones.

---

## Autores

- [Tu Nombre]
- [Colaboradores]

---

## Licencia

Este proyecto está bajo la licencia MIT.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## Contacto

¿Dudas o sugerencias?  
Escríbenos a [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)

---

¡Gracias por usar **SmartRoom**!