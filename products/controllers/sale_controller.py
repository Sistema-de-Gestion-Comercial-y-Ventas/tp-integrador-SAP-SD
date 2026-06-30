import logging

from django.http import JsonResponse

from products.services.sale_service import SaleService
from products.exceptions.sale_exception import SaleNotFoundException

logger = logging.getLogger(__name__)


class SaleController:
    """
    Controller de ventas.
    Recibe peticiones HTTP, delega al Service y devuelve respuestas JSON.
    """

    def __init__(self):
        self.service = SaleService()

    def get_sales(self, _request):
        """Maneja GET /sales/. Devuelve la lista completa de ventas en formato JSON."""
        logger.info("GET /sales/ - Consultando lista de ventas")

        try:
            sales_dtos = self.service.get_sales()

            data = []

            for sale_dto in sales_dtos:
                data.append(sale_dto.to_dict())

            logger.info("GET /sales/ - %s ventas encontradas", len(data))

            return JsonResponse(data, safe=False, status=200)

        except Exception as error:
            logger.error("Error en get_sales: %s", error)

            return JsonResponse(
                {"error": "Error interno del servidor"},
                status=500
            )

    def get_sale_by_id(self, _request, sale_id):
        """Maneja GET /sales/<id>/. Devuelve una venta específica en formato JSON."""
        logger.info("GET /sales/%s/ - Consultando venta por ID", sale_id)

        try:
            sale_dto = self.service.get_sale_by_id(sale_id)

            if sale_dto is None:
                raise SaleNotFoundException(sale_id)

            return JsonResponse(sale_dto.to_dict(), status=200)

        except SaleNotFoundException as error:
            logger.warning("Venta no encontrada: %s", error.message)

            return JsonResponse(
                {"error": error.message},
                status=error.status_code
            )

        except Exception as error:
            logger.error("Error en get_sale_by_id: %s", error)

            return JsonResponse(
                {"error": "Error interno del servidor"},
                status=500
            )