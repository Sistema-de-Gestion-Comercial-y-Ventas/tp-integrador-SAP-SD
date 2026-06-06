import logging   

from django.http import JsonResponse   

from products.services.product_service import ProductService     


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