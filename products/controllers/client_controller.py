import json
import logging

from django.http import JsonResponse

from products.dto.client_dto import ClientDTO
from products.exceptions.client_exception import ClientAlreadyExistsException, ClientNotFoundException
from products.services.client_service import ClientService

logger = logging.getLogger(__name__)


class ClientController:
    """
    Controller de clientes.
    Recibe peticiones HTTP, delega al Service y devuelve respuestas JSON.
    """

    def __init__(self):
        self.service = ClientService()

    def client_collection(self, request):
        """Maneja GET y POST sobre /clients/."""
        if request.method == 'GET':
            return self.get_clients(request)
        if request.method == 'POST':
            return self.create_client(request)
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)

    def get_clients(self, _request):
        logger.info("GET /clients/ - Consultando lista de clientes")

        try:
            clients = self.service.get_clients()

            data = []
            for client in clients:
                data.append({
                    "id": client.id,
                    "name": client.name,
                    "email": client.email,
                    "phone": client.phone
                })

            logger.info("GET /clients/ - %s clientes encontrados", len(data))
            return JsonResponse(data, safe=False, status=200)

        except Exception as error:
            logger.error("Error en get_clients: %s", error)
            return JsonResponse({"error": "Error interno del servidor"}, status=500)

    def get_client_by_id(self, _request, client_id):
        logger.info("GET /clients/%s/ - Buscando cliente", client_id)

        try:
            client = self.service.get_client_by_id(client_id)
            if client is None:
                raise ClientNotFoundException(client_id)

            dto = ClientDTO(client.id, client.name, client.email, client.phone)
            logger.info("GET /clients/%s/ - Cliente encontrado", client_id)
            return JsonResponse(dto.to_dict(), status=200)

        except ClientNotFoundException as error:
            logger.warning("GET /clients/%s/ - %s", client_id, error.message)
            return JsonResponse({"error": error.message}, status=error.status_code)

        except Exception as error:
            logger.error("Error en get_client_by_id: %s", error)
            return JsonResponse({"error": "Error interno del servidor"}, status=500)

    def create_client(self, request):
        logger.info("POST /clients/ - Creando cliente")

        try:
            data = json.loads(request.body)
            client_id = data.get('id')
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')

            client = self.service.create_client(client_id, name, email, phone)
            dto = ClientDTO(client.id, client.name, client.email, client.phone)

            logger.info("POST /clients/ - Cliente creado correctamente")
            return JsonResponse(dto.to_dict(), status=201)

        except ClientAlreadyExistsException as error:
            logger.warning("POST /clients/ - %s", error.message)
            return JsonResponse({"error": error.message}, status=error.status_code)

        except ValueError as error:
            logger.warning("POST /clients/ - %s", error)
            return JsonResponse({"error": str(error)}, status=400)

        except Exception as error:
            logger.error("Error en create_client: %s", error)
            return JsonResponse({"error": "Error interno del servidor"}, status=500)

    def client_detail(self, request, client_id):
        if request.method == 'GET':
            return self.get_client_by_id(request, client_id)
        if request.method == 'PUT':
            return self.update_client(request, client_id)
        if request.method == 'DELETE':
            return self.delete_client(request, client_id)
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)

    def update_client(self, request, client_id):
        logger.info("PUT /clients/%s/ - Actualizando cliente", client_id)

        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')

            client = self.service.update_client(client_id, name, email, phone)
            if client is None:
                raise ClientNotFoundException(client_id)

            dto = ClientDTO(client.id, client.name, client.email, client.phone)
            logger.info("PUT /clients/%s/ - Cliente actualizado correctamente", client_id)
            return JsonResponse(dto.to_dict(), status=200)

        except ClientNotFoundException as error:
            logger.warning("PUT /clients/%s/ - %s", client_id, error.message)
            return JsonResponse({"error": error.message}, status=error.status_code)

        except ValueError as error:
            logger.warning("PUT /clients/%s/ - %s", client_id, error)
            return JsonResponse({"error": str(error)}, status=400)

        except Exception as error:
            logger.error("Error en update_client: %s", error)
            return JsonResponse({"error": "Error interno del servidor"}, status=500)

    def delete_client(self, request, client_id):
        logger.info("DELETE /clients/%s/ - Eliminando cliente", client_id)

        try:
            deleted = self.service.delete_client(client_id)
            if not deleted:
                raise ClientNotFoundException(client_id)

            logger.info("DELETE /clients/%s/ - Cliente eliminado correctamente", client_id)
            return JsonResponse({'message': 'Cliente eliminado correctamente.'}, status=200)

        except ClientNotFoundException as error:
            logger.warning("DELETE /clients/%s/ - %s", client_id, error.message)
            return JsonResponse({"error": error.message}, status=error.status_code)

        except Exception as error:
            logger.error("Error en delete_client: %s", error)
            return JsonResponse({"error": "Error interno del servidor"}, status=500)