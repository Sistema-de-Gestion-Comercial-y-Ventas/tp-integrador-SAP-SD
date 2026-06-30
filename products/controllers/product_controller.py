import json
import logging

from django.http import JsonResponse

from products.dto.product_dto import ProductDTO
from products.exceptions.product_exception import ProductException, ProductNotFoundException
from products.services.product_service import ProductService


logger = logging.getLogger(__name__)


class ProductController:
    """Controller de productos. Recibe peticiones HTTP, delega al Service y devuelve respuestas JSON."""

    def __init__(self):
        self.service = ProductService()

    def products(self, request):
        """Despacha operaciones sobre la coleccion publica de productos."""
        if request.method == 'GET':
            return self.get_products(request)

        if request.method == 'POST':
            return self.create_product(request)

        return JsonResponse({'error': 'Metodo no permitido'}, status=405)

    def product_detail(self, request, product_id):
        """Despacha operaciones sobre un producto puntual."""
        if request.method == 'GET':
            return self.get_product_by_id(request, product_id)

        if request.method == 'PUT':
            return self.update_product(request, product_id)

        if request.method == 'DELETE':
            return self.delete_product(request, product_id)

        return JsonResponse({'error': 'Metodo no permitido'}, status=405)

    def admin_product_detail(self, request, product_id):
        """Despacha operaciones administrativas sobre un producto puntual."""
        if request.method == 'PUT':
            return self.update_product(request, product_id)

        if request.method == 'DELETE':
            return self.delete_product(request, product_id)

        return JsonResponse({'error': 'Metodo no permitido'}, status=405)

    def get_products(self, _request):
        """Maneja GET /products/. Devuelve la lista completa de productos en formato JSON."""
        logger.info('GET /products/ - Consultando lista de productos')

        try:
            products = self.service.get_products()
            data = [
                {
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                }
                for product in products
            ]

            logger.info('GET /products/ - %s productos encontrados', len(data))
            return JsonResponse(data, safe=False, status=200)

        except Exception as error:
            logger.error('Error en get_products: %s', error)
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def get_product_by_id(self, _request, product_id):
        """Maneja GET /products/<id>/. Devuelve un producto por su ID."""
        logger.info('GET /products/%s/ - Buscando producto', product_id)

        try:
            product = self.service.get_product_by_id(product_id)

            if product is None:
                raise ProductNotFoundException(product_id)

            dto = ProductDTO(product.id, product.name, product.price)

            logger.info('GET /products/%s/ - Producto encontrado', product_id)
            return JsonResponse(dto.to_dict(), status=200)

        except ProductNotFoundException as error:
            logger.warning('GET /products/%s/ - %s', product_id, error.message)
            return JsonResponse({'error': error.message}, status=error.status_code)

        except Exception as error:
            logger.error('Error en get_product_by_id: %s', error)
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def create_product(self, request):
        """Maneja POST /products/ y POST /admin/products/."""
        logger.info('POST %s - Creando producto', request.path)

        if request.method != 'POST':
            return JsonResponse({'error': 'Metodo no permitido'}, status=405)

        try:
            payload = self._get_json_payload(request)

            if request.path.startswith('/admin/products/'):
                product = self.service.create_product(
                    payload.get('id'),
                    payload.get('name'),
                    payload.get('price'),
                )
            else:
                product = self.service.create_product(
                    payload.get('name'),
                    payload.get('price'),
                )

            dto = ProductDTO(product.id, product.name, product.price)

            logger.info('POST %s - Producto creado con ID %s', request.path, product.id)
            return JsonResponse(dto.to_dict(), status=201)

        except ProductException as error:
            logger.warning('POST %s - %s', request.path, error.message)
            return JsonResponse({'error': error.message}, status=error.status_code)

        except json.JSONDecodeError:
            logger.warning('POST %s - JSON invalido', request.path)
            return JsonResponse({'error': 'JSON invalido'}, status=400)

        except Exception as error:
            logger.error('Error en create_product: %s', error)
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def update_product(self, request, product_id):
        """Maneja PUT /products/<id>/ y PUT /admin/products/<id>/."""
        logger.info('PUT %s - Actualizando producto', request.path)

        try:
            payload = self._get_json_payload(request)
            product = self.service.update_product(
                product_id,
                payload.get('name'),
                payload.get('price'),
            )
            dto = ProductDTO(product.id, product.name, product.price)

            logger.info('PUT %s - Producto actualizado', request.path)
            return JsonResponse(dto.to_dict(), status=200)

        except ProductException as error:
            logger.warning('PUT %s - %s', request.path, error.message)
            return JsonResponse({'error': error.message}, status=error.status_code)

        except json.JSONDecodeError:
            logger.warning('PUT %s - JSON invalido', request.path)
            return JsonResponse({'error': 'JSON invalido'}, status=400)

        except Exception as error:
            logger.error('Error en update_product: %s', error)
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def delete_product(self, request, product_id):
        """Maneja DELETE /products/<id>/ y DELETE /admin/products/<id>/."""
        logger.info('DELETE %s - Eliminando producto', request.path)

        try:
            self.service.delete_product(product_id)

            logger.info('DELETE %s - Producto eliminado', request.path)
            return JsonResponse({'message': 'Producto eliminado correctamente.'}, status=200)

        except ProductException as error:
            logger.warning('DELETE %s - %s', request.path, error.message)
            return JsonResponse({'error': error.message}, status=error.status_code)

        except Exception as error:
            logger.error('Error en delete_product: %s', error)
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def _get_json_payload(self, request):
        """Obtiene el cuerpo JSON de una peticion HTTP."""
        body = request.body.decode('utf-8')

        if not body:
            return {}

        return json.loads(body)
