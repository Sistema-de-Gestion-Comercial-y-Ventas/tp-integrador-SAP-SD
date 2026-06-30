import json
import logging

from django.http import JsonResponse

from products.services.product_service import ProductService
from products.dto.product_dto import ProductDTO
from products.exceptions.product_exception import ProductNotFoundException


# Obtener un logger para este módulo.
# El nombre __name__ se convierte en 'products.controllers.product_controller'

logger = logging.getLogger(__name__)


class ProductController:
    """Controller de productos. Recibe peticiones HTTP, delega al Service y devuelve respuestas JSON."""

    def __init__(self):
        self.service = ProductService()

    def get_products(self, _request):
        """Maneja GET /products/. Devuelve la lista completa de productos en formato JSON."""
        logger.info('GET /products/ - Consultando lista de productos')

        try:
            products = self.service.get_products()

            data = []
            for product in products:
                data.append({
                    'id': product.product_id,
                    'name': product.name,
                    'price': product.price,
                })

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

            dto = ProductDTO(product.product_id, product.name, product.price)

            logger.info('GET /products/%s/ - Producto encontrado', product_id)
            return JsonResponse(dto.to_dict(), status=200)

        except ProductNotFoundException as error:
            logger.warning('GET /products/%s/ - %s', product_id, error.message)
            return JsonResponse({'error': error.message}, status=error.status_code)

        except Exception as error:
            logger.error('Error en get_product_by_id: %s', error)
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def create_product(self, request):
        """Maneja POST /admin/products/. Crea un producto nuevo."""
        if request.method != 'POST':
            return JsonResponse({'error': 'Método no permitido'}, status=405)

        logger.info('POST /admin/products/ - Creando producto')

        try:
            data = json.loads(request.body)
            product_id = data.get('id')
            name = data.get('name')
            price = data.get('price')

            product = self.service.create_product(product_id, name, price)
            dto = ProductDTO(product.product_id, product.name, product.price)

            logger.info('POST /admin/products/ - Producto creado correctamente')
            return JsonResponse(dto.to_dict(), status=201)

        except ValueError as error:
            logger.warning('POST /admin/products/ - %s', error)
            return JsonResponse({'error': str(error)}, status=400)

        except Exception as error:
            logger.error('Error en create_product: %s', error)
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def admin_product_detail(self, request, product_id):
        """Maneja PUT y DELETE sobre /admin/products/<id>/."""
        if request.method == 'PUT':
            return self.update_product(request, product_id)
        if request.method == 'DELETE':
            return self.delete_product(request, product_id)
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    def update_product(self, request, product_id):
        """Actualiza un producto existente."""
        logger.info('PUT /admin/products/%s/ - Actualizando producto', product_id)

        try:
            data = json.loads(request.body)
            name = data.get('name')
            price = data.get('price')

            product = self.service.update_product(product_id, name, price)
            if product is None:
                raise ProductNotFoundException(product_id)

            dto = ProductDTO(product.product_id, product.name, product.price)

            logger.info('PUT /admin/products/%s/ - Producto actualizado correctamente', product_id)
            return JsonResponse(dto.to_dict(), status=200)

        except ProductNotFoundException as error:
            logger.warning('PUT /admin/products/%s/ - %s', product_id, error.message)
            return JsonResponse({'error': error.message}, status=error.status_code)

        except ValueError as error:
            logger.warning('PUT /admin/products/%s/ - %s', product_id, error)
            return JsonResponse({'error': str(error)}, status=400)

        except Exception as error:
            logger.error('Error en update_product: %s', error)
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def delete_product(self, request, product_id):
        """Elimina un producto existente."""
        logger.info('DELETE /admin/products/%s/ - Eliminando producto', product_id)

        try:
            deleted = self.service.delete_product(product_id)
            if not deleted:
                raise ProductNotFoundException(product_id)

            logger.info('DELETE /admin/products/%s/ - Producto eliminado correctamente', product_id)
            return JsonResponse({'message': 'Producto eliminado correctamente.'}, status=200)

        except ProductNotFoundException as error:
            logger.warning('DELETE /admin/products/%s/ - %s', product_id, error.message)
            return JsonResponse({'error': error.message}, status=error.status_code)

        except Exception as error:
            logger.error('Error en delete_product: %s', error)
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)


