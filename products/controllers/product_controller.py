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
