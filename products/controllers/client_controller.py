import logging

from django.http import JsonResponse

from products.services.client_service import ClientService

logger = logging.getLogger(__name__)


class ClientController:
    """
    Controller de clientes.
    Recibe peticiones HTTP, delega al Service y devuelve respuestas JSON.
    """

    def __init__(self):
        self.service = ClientService()

    def get_clients(self, _request):

        logger.info("GET /clients/ - Consultando lista de clientes")

        try:
            clients = self.service.get_clients()

            data = []

            for client in clients:
                data.append({
                    "id": client.client_id,
                    "name": client.name,
                    "email": client.email,
                    "phone": client.phone
                })

            logger.info(
                "GET /clients/ - %s clientes encontrados",
                len(data)
            )

            return JsonResponse(data, safe=False, status=200)

        except Exception as error:
            logger.error("Error en get_clients: %s", error)

            return JsonResponse(
                {"error": "Error interno del servidor"},
                status=500
            )