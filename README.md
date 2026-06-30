TP Integrador - Sistema de Gestión Comercial y Ventas
Universidad Escuela Argentina de Negocios (UEAN)
Lic. en Tecnología Informática - Introducción al Desarrollo de Software 2026
Descripción del Proyecto
Sistema backend desarrollado con Django y complementado con FastAPI, orientado a la gestión comercial y de ventas.
El sistema permite administrar productos, clientes y operaciones comerciales, utilizando una arquitectura por capas y persistencia mediante Django ORM. Para el entorno con contenedores se utiliza PostgreSQL mediante Docker Compose.
Tecnologías utilizadas
•	Python 3
•	Django
•	Django ORM
•	FastAPI
•	Uvicorn
•	PostgreSQL
•	Docker
•	Docker Compose
•	JSON REST
•	Git y GitHub
Arquitectura del Proyecto
El proyecto sigue una arquitectura modular por capas:
HTTP Request
     |
 Controller        <- recibe la petición HTTP y devuelve respuestas JSON
     |
 Service           <- contiene la lógica de negocio
     |
 Repository        <- accede a los datos mediante Django ORM
     |
 Model             <- define las entidades del sistema
     |
 Database          <- PostgreSQL / base configurada por Django

Módulos principales:
•	Productos
•	Clientes
•	Ventas
•	API complementaria con FastAPI
Ejecución local con Django
1. Activar el entorno virtual
.\venv\Scripts\activate

2. Instalar dependencias
pip install -r requirements.txt

3. Aplicar migraciones
python manage.py migrate

4. Levantar el servidor de Django
python manage.py runserver

El servidor queda disponible en:
http://127.0.0.1:8000/

Ejecución con FastAPI
FastAPI funciona como API complementaria y reutiliza la lógica existente del proyecto Django.
Con el entorno virtual activado, ejecutar:
python -m uvicorn fastapi_app.main:app --reload --port 8001

La API queda disponible en:
http://127.0.0.1:8001/

Endpoints principales de FastAPI:
http://127.0.0.1:8001/products
http://127.0.0.1:8001/clients
http://127.0.0.1:8001/sales

Ejecución con Docker
El proyecto incluye configuración con Docker Compose para levantar Django junto con PostgreSQL.
docker compose up --build

Para detener los servicios:
docker compose down

Servicios incluidos:
•	django: aplicación Django disponible en http://127.0.0.1:8000/
•	postgres: base de datos PostgreSQL
Endpoints disponibles en Django
Método	URL	Descripción
GET	/products/	Lista todos los productos
GET	/products/<id>/	Obtiene un producto por ID
POST	/products/	Crea un producto
PUT	/products/<id>/	Modifica un producto existente
DELETE	/products/<id>/	Elimina un producto existente
POST	/admin/products/	Crea un producto indicando ID
PUT	/admin/products/<id>/	Modifica un producto desde ruta administrativa
DELETE	/admin/products/<id>/	Elimina un producto desde ruta administrativa
GET	/clients/	Lista todos los clientes
GET	/clients/<id>/	Obtiene un cliente por ID
POST	/clients/	Crea un cliente
PUT	/clients/<id>/	Modifica un cliente
DELETE	/clients/<id>/	Elimina un cliente
GET	/sales/	Lista todas las ventas
GET	/sales/<id>/	Obtiene una venta por ID
POST	/sales/	Crea una venta

Endpoints disponibles en FastAPI
Método	URL	Descripción
GET	/	Endpoint inicial de prueba
GET	/products	Lista todos los productos
GET	/products/{product_id}	Obtiene un producto por ID
GET	/clients	Lista todos los clientes
GET	/sales	Lista todas las ventas
GET	/sales/{sale_id}	Obtiene una venta por ID

Ejemplos de uso
Crear un producto
Invoke-RestMethod -Uri "http://127.0.0.1:8000/products/" -Method POST -ContentType "application/json" -Body '{"name":"Mouse Gamer","price":15000}'

Ejemplo de respuesta:
{
  "id": 1,
  "name": "Mouse Gamer",
  "price": 15000
}

Crear un cliente
Invoke-RestMethod -Uri "http://127.0.0.1:8000/clients/" -Method POST -ContentType "application/json" -Body '{"id":1,"name":"Juan Perez","email":"juan.perez@gmail.com","phone":"1122334455"}'

Ejemplo de respuesta:
{
  "id": 1,
  "name": "Juan Perez",
  "email": "juan.perez@gmail.com",
  "phone": "1122334455"
}

Crear una venta
Invoke-RestMethod -Uri "http://127.0.0.1:8000/sales/" -Method POST -ContentType "application/json" -Body '{"client_id":1,"product_id":1,"quantity":2,"status":"pendiente"}'

Ejemplo de respuesta:
{
  "id": 1,
  "client_id": 1,
  "product_id": 1,
  "quantity": 2,
  "status": "pendiente",
  "total": 30000
}

Validaciones y manejo de errores
El sistema incluye validaciones para evitar datos incompletos o inconsistentes. También utiliza excepciones personalizadas y respuestas JSON con códigos HTTP adecuados.
Ejemplos de respuestas posibles:
•	200 OK
•	201 Created
•	400 Bad Request
•	404 Not Found
•	405 Method Not Allowed
•	409 Conflict
•	500 Internal Server Error
Logging
El proyecto utiliza logging en las capas principales para registrar operaciones, errores y eventos relevantes durante la ejecución.
Estado actual
El sistema permite:
•	Administrar productos.
•	Administrar clientes.
•	Registrar y consultar ventas.
•	Calcular el total de una venta según producto y cantidad.
•	Consultar datos desde Django.
•	Consultar datos desde FastAPI.
•	Ejecutar el proyecto localmente.
•	Ejecutar el proyecto mediante Docker con PostgreSQL.

