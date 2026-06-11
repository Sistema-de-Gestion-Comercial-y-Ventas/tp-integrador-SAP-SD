# TP Integrador — Sistema de Gestión Comercial y Ventas (SAP SD)

**Universidad Escuela Argentina de Negocios (UEAN)**  
Lic. en Tecnología Informática — Introducción al Desarrollo de Software 2026  

---

## Integrantes

| Alumno | Módulo |
|---|---|
| Facu | Módulo de Clientes (`clients`) |
| Emiliano | Módulo de Productos (`products`) |

---

## Descripción del Proyecto

Sistema backend desarrollado con **Django** que simula un módulo de gestión comercial inspirado en SAP SD (Sales & Distribution). Expone una API REST que permite consultar productos y clientes almacenados en memoria.

Los datos se gestionan en memoria (listas Python) en esta fase inicial, preparando la arquitectura para conectar una base de datos PostgreSQL en clases futuras.

---

## Cómo ejecutar el proyecto

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

## Endpoints disponibles

| Método | URL | Descripción | Respuesta |
|---|---|---|---|
| GET | `/products/` | Lista todos los productos | 200 OK — array JSON |
| GET | `/products/<id>/` | Obtiene un producto por ID | 200 OK o 404 Not Found |
| GET | `/clients/` | Lista todos los clientes | 200 OK — array JSON |

### Ejemplos de respuesta

**GET /products/**
```json
[
  { "id": 1, "name": "Mouse Gamer", "price": 15000 },
  { "id": 2, "name": "Teclado Mecanico", "price": 45000 },
  { "id": 3, "name": "Smart Watch", "price": 120000 }
]
```

**GET /products/1/**
```json
{ "id": 1, "name": "Mouse Gamer", "price": 15000 }
```

**GET /products/99/** *(producto inexistente)*
```json
{ "error": "Producto con ID 99 no encontrado." }
```

---

## Arquitectura del Módulo de Productos

El módulo sigue una **arquitectura backend por capas**, donde cada archivo tiene una única responsabilidad. Esto facilita el mantenimiento y la extensión del sistema.

```
HTTP Request
     ↓
 Controller        ← recibe la petición HTTP, devuelve JSON
     ↓
  Service          ← contiene la lógica de negocio
     ↓
 Repository        ← accede a los datos (lista en memoria)
     ↓
   Model           ← define la entidad Product
```

---

## Descripción de cada capa

### Model — `products/models/product.py`

Define la entidad `Product`: qué es un producto y qué datos tiene.

```python
class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id  # Identificador único
        self.name = name              # Nombre del producto
        self.price = price            # Precio en pesos
```

> No hereda de `django.db.models.Model` porque en esta fase los datos se almacenan en memoria. En clases futuras se migrará a PostgreSQL.

---

### Repository — `products/repositories/product_repository.py`

Simula una base de datos usando una lista de objetos en memoria. Provee métodos para acceder a los datos sin que el resto del sistema sepa cómo están almacenados.

```python
class ProductRepository:
    products = [
        Product(1, 'Mouse Gamer', 15000),
        Product(2, 'Teclado Mecanico', 45000),
        Product(3, 'Smart Watch', 120000),
    ]

    def find_all(self):
        return self.products

    def find_by_id(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
```

> Si en el futuro se cambia la fuente de datos a PostgreSQL, **solo se modifica esta capa**, sin tocar el Service ni el Controller.

---

### Service — `products/services/product_service.py`

Contiene la lógica de negocio. Coordina el acceso a datos a través del Repository. En sistemas reales, aquí se aplicarían descuentos, validaciones de stock, notificaciones, etc.

```python
class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def get_products(self):
        return self.repository.find_all()

    def get_product_by_id(self, product_id):
        return self.repository.find_by_id(product_id)
```

---

### DTO — `products/dto/product_dto.py`

Data Transfer Object: define exactamente qué campos se exponen al cliente. Permite ocultar campos internos del modelo (como costos, datos sensibles) sin modificar la entidad.

```python
class ProductDTO:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            'id': self.product_id,
            'name': self.name,
            'price': self.price,
        }
```

---

### Validator — `products/validators/product_validator.py`

Verifica que los datos de entrada cumplen las reglas de negocio antes de procesarlos.

```python
class ProductValidator:
    def validate_name(self, name):
        if not name or len(name.strip()) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres.')

    def validate_price(self, price):
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError('El precio debe ser un número mayor a cero.')
```

---

### Exception — `products/exceptions/product_exception.py`

Errores personalizados del dominio de productos. Permiten diferenciar un "producto no encontrado" de un error genérico del servidor.

```python
class ProductException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ProductNotFoundException(ProductException):
    def __init__(self, product_id):
        super().__init__(
            message=f'Producto con ID {product_id} no encontrado.',
            status_code=404
        )
```

---

### Controller — `products/controllers/product_controller.py`

Punto de entrada HTTP. Recibe las peticiones, delega al Service y devuelve respuestas JSON. Usa el DTO para serializar los datos y las excepciones para manejar errores.

```python
class ProductController:
    def __init__(self):
        self.service = ProductService()

    def get_products(self, _request):
        # Devuelve la lista completa de productos
        products = self.service.get_products()
        data = [{'id': p.product_id, 'name': p.name, 'price': p.price} for p in products]
        return JsonResponse(data, safe=False, status=200)

    def get_product_by_id(self, _request, product_id):
        # Busca un producto por ID, lanza 404 si no existe
        product = self.service.get_product_by_id(product_id)
        if product is None:
            raise ProductNotFoundException(product_id)
        dto = ProductDTO(product.product_id, product.name, product.price)
        return JsonResponse(dto.to_dict(), status=200)
```

---

### URLs — `config/urls.py`

Conecta cada URL con su método del Controller.

```python
path('products/', controller.get_products),
path('products/<int:product_id>/', controller.get_product_by_id),
```

---

## Estructura de archivos del módulo products

```
products/
├── controllers/
│   └── product_controller.py   ← recibe HTTP, responde JSON
├── services/
│   └── product_service.py      ← lógica de negocio
├── repositories/
│   └── product_repository.py   ← acceso a datos
├── models/
│   └── product.py              ← entidad Product
├── dto/
│   └── product_dto.py          ← qué datos se exponen
├── validators/
│   └── product_validator.py    ← validaciones de entrada
└── exceptions/
    └── product_exception.py    ← errores del dominio
```

---

## Tecnologías utilizadas

- **Python 3.x**
- **Django 6.0.6**
- **SQLite** (base de datos interna de Django para sesiones y admin)
- **JSON** como formato de respuesta de la API
