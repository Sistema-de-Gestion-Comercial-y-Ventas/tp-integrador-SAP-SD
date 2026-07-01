TP Integrador - Sistema de GestiÃ³n Comercial y Ventas
Universidad Escuela Argentina de Negocios (UEAN)
Lic. en TecnologÃ­a InformÃ¡tica - IntroducciÃ³n al Desarrollo de Software 2026
DescripciÃ³n del Proyecto
Sistema backend desarrollado con Django y complementado con FastAPI, orientado a la gestiÃ³n comercial y de ventas.
El sistema permite administrar productos, clientes y operaciones comerciales, utilizando una arquitectura por capas y persistencia mediante Django ORM. Para el entorno con contenedores se utiliza PostgreSQL mediante Docker Compose.
TecnologÃ­as utilizadas
â€¢	Python 3
â€¢	Django
â€¢	Django ORM
â€¢	FastAPI
â€¢	Uvicorn
â€¢	PostgreSQL
â€¢	Docker
â€¢	Docker Compose
â€¢	JSON REST
â€¢	Git y GitHub
Arquitectura del Proyecto
El proyecto sigue una arquitectura modular por capas:
HTTP Request
     |
 Controller        <- recibe la peticiÃ³n HTTP y devuelve respuestas JSON
     |
 Service           <- contiene la lÃ³gica de negocio
     |
 Repository        <- accede a los datos mediante Django ORM
     |
 Model             <- define las entidades del sistema
     |
 Database          <- PostgreSQL / base configurada por Django

MÃ³dulos principales:
â€¢	Productos
â€¢	Clientes
â€¢	Ventas
â€¢	API complementaria con FastAPI
EjecuciÃ³n local con Django
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

EjecuciÃ³n con FastAPI
FastAPI funciona como API complementaria y reutiliza la lÃ³gica existente del proyecto Django.
Con el entorno virtual activado, ejecutar:
python -m uvicorn fastapi_app.main:app --reload --port 8001

La API queda disponible en:
http://127.0.0.1:8001/

Endpoints principales de FastAPI:
http://127.0.0.1:8001/products
http://127.0.0.1:8001/clients
http://127.0.0.1:8001/sales

EjecuciÃ³n con Docker
El proyecto incluye configuraciÃ³n con Docker Compose para levantar Django junto con PostgreSQL.
docker compose up --build

Para detener los servicios:
docker compose down

Servicios incluidos:
â€¢	django: aplicaciÃ³n Django disponible en http://127.0.0.1:8000/
â€¢	postgres: base de datos PostgreSQL
Endpoints disponibles en Django
MÃ©todo	URL	DescripciÃ³n
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
PUT	/sales/<id>/	Modifica una venta
DELETE	/sales/<id>/	Elimina una venta

Endpoints disponibles en FastAPI
MÃ©todo	URL	DescripciÃ³n
GET	/	Endpoint inicial de prueba
GET	/products	Lista todos los productos
GET	/products/{product_id}	Obtiene un producto por ID
POST	/products	Crea un producto
PUT	/products/{product_id}	Modifica un producto
DELETE	/products/{product_id}	Elimina un producto
GET	/clients	Lista todos los clientes
GET	/clients/{client_id}	Obtiene un cliente por ID
POST	/clients	Crea un cliente
PUT	/clients/{client_id}	Modifica un cliente
DELETE	/clients/{client_id}	Elimina un cliente
GET	/sales	Lista todas las ventas
GET	/sales/{sale_id}	Obtiene una venta por ID
POST	/sales	Crea una venta
PUT	/sales/{sale_id}	Modifica una venta
DELETE	/sales/{sale_id}	Elimina una venta

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
Invoke-RestMethod -Uri "http://127.0.0.1:8000/sales/" -Method POST -ContentType "application/json" -Body '{"client_id":1,"product_id":1,"quantity":2,"status":"pending"}'

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
El sistema incluye validaciones para evitar datos incompletos o inconsistentes. TambiÃ©n utiliza excepciones personalizadas y respuestas JSON con cÃ³digos HTTP adecuados.
Ejemplos de respuestas posibles:
â€¢	200 OK
â€¢	201 Created
â€¢	400 Bad Request
â€¢	404 Not Found
â€¢	405 Method Not Allowed
â€¢	409 Conflict
â€¢	500 Internal Server Error
Logging
El proyecto utiliza logging en las capas principales para registrar operaciones, errores y eventos relevantes durante la ejecuciÃ³n.
Estado actual
El sistema permite:
â€¢	Administrar productos.
â€¢	Administrar clientes.
â€¢	Registrar y consultar ventas.
â€¢	Calcular el total de una venta segÃºn producto y cantidad.
â€¢	Consultar datos desde Django.
â€¢	Consultar datos desde FastAPI.
â€¢	Ejecutar el proyecto localmente.
â€¢	Ejecutar el proyecto mediante Docker con PostgreSQL.


