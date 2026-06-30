# TP Integrador - Sistema de Gestion Comercial y Ventas (SAP SD)

**Universidad Escuela Argentina de Negocios (UEAN)**  
Lic. en Tecnologia Informatica - Introduccion al Desarrollo de Software 2026

---

## Descripcion del Proyecto

Sistema backend desarrollado con **Django** que simula un modulo de gestion comercial inspirado en SAP SD (Sales & Distribution). Expone una API REST que permite consultar y administrar productos, clientes y operaciones comerciales almacenadas en memoria.

Los datos se gestionan en memoria (listas Python) en esta fase inicial, preparando la arquitectura para conectar una base de datos PostgreSQL en clases futuras.

---

## Como ejecutar el proyecto

```bash
# 1. Activar el entorno virtual
.\venv\Scripts\activate

# 2. Aplicar migraciones iniciales (solo la primera vez)
python manage.py migrate

# 3. Iniciar el servidor de desarrollo
python manage.py runserver
```

El servidor queda disponible en `http://127.0.0.1:8000/`

---

## Ejecucion con Docker

El proyecto incluye una configuracion base con Django y PostgreSQL para desarrollo local.

```bash
# Construir y levantar los servicios
docker compose up --build

# Detener los servicios
docker compose down
```

Servicios incluidos:

- `web`: aplicacion Django disponible en `http://127.0.0.1:8000/`
- `db`: PostgreSQL disponible en el puerto `5432`

> La configuracion de PostgreSQL queda preparada en Docker Compose. La conexion final desde Django se completa cuando el modulo de ORM/PostgreSQL actualice `config/settings.py`.

---

## Endpoints disponibles

| Metodo | URL | Descripcion | Respuesta |
|---|---|---|---|
| GET | `/products/` | Lista todos los productos | 200 OK - array JSON |
| GET | `/products/<id>/` | Obtiene un producto por ID | 200 OK o 404 Not Found |
| POST | `/products/` | Crea un producto con ID automatico | 201 Created, 400 Bad Request o 409 Conflict |
| PUT | `/products/<id>/` | Modifica un producto existente | 200 OK, 400 Bad Request, 404 Not Found o 409 Conflict |
| DELETE | `/products/<id>/` | Elimina un producto existente | 200 OK o 404 Not Found |
| POST | `/admin/products/` | Crea un producto indicando ID | 201 Created, 400 Bad Request o 409 Conflict |
| PUT | `/admin/products/<id>/` | Modifica un producto desde ruta administrativa | 200 OK, 400 Bad Request, 404 Not Found o 409 Conflict |
| DELETE | `/admin/products/<id>/` | Elimina un producto desde ruta administrativa | 200 OK o 404 Not Found |
| GET | `/clients/` | Lista todos los clientes | 200 OK - array JSON |
| GET | `/clients/<id>/` | Obtiene un cliente por ID | 200 OK o 404 Not Found |
| POST | `/clients/` | Crea un cliente | 201 Created o error de validacion |
| PUT | `/clients/<id>/` | Modifica un cliente | 200 OK o error |
| DELETE | `/clients/<id>/` | Elimina un cliente | 200 OK o 404 Not Found |
| GET | `/sales/` | Lista todas las ventas | 200 OK - array JSON |
| GET | `/sales/<id>/` | Obtiene una venta por ID | 200 OK o 404 Not Found |

### Ejemplos de productos

**GET /products/**
```json
[
  { "id": 1, "name": "Mouse Gamer", "price": 15000 },
  { "id": 2, "name": "Teclado Mecanico", "price": 45000 },
  { "id": 3, "name": "Smart Watch", "price": 120000 }
]
```

**POST /products/**
```json
{
  "name": "Monitor LED",
  "price": 90000
}
```

Respuesta esperada:
```json
{ "id": 4, "name": "Monitor LED", "price": 90000 }
```

**PUT /products/4/**
```json
{
  "name": "Monitor LED 24",
  "price": 110000
}
```

**DELETE /products/4/**
```json
{ "message": "Producto eliminado correctamente." }
```

---

## Arquitectura del Modulo de Productos

El modulo sigue una arquitectura backend por capas, donde cada archivo tiene una unica responsabilidad.

```text
HTTP Request
     |
 Controller        <- recibe la peticion HTTP, devuelve JSON
     |
  Service          <- contiene la logica de negocio
     |
 Repository        <- accede a los datos (lista en memoria)
     |
   Model           <- define la entidad Product
```

---

## Tecnologias utilizadas

- **Python 3.x**
- **Django 6.0.6**
- **SQLite** (base de datos interna de Django para sesiones y admin)
- **JSON** como formato de respuesta de la API
