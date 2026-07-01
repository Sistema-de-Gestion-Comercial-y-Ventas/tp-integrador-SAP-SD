import logging

from products.exceptions.client_exception import ClientAlreadyExistsException
from products.models.client import Client

logger = logging.getLogger(__name__)


class ClientRepository:
    """
    Repositorio de clientes usando Django ORM.
    Consulta a PostgreSQL a traves del ORM de Django.
    """

    def find_all(self):
        """Devuelve todos los clientes registrados."""
        logger.info("Repository clientes - Consultando todos los clientes")
        return Client.objects.all().order_by('id')

    def find_by_id(self, client_id):
        """Busca un cliente por su ID. Devuelve None si no existe."""
        try:
            return Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            logger.warning("Repository clientes - Cliente con ID %s no encontrado", client_id)
            return None

    def create(self, name, email, phone):
        """Crea un nuevo cliente."""
        try:
            # Verificar si ya existe un cliente con este email
            Client.objects.get(email=email)
            raise ClientAlreadyExistsException(email)
        except Client.DoesNotExist:
            pass

        client = Client.objects.create(name=name, email=email, phone=phone)
        logger.info("Repository clientes - Cliente %s creado", client.id)
        return client

    def update(self, client_id, name, email, phone):
        """Actualiza los datos de un cliente existente."""
        try:
            client = Client.objects.get(id=client_id)
            client.name = name
            client.email = email
            client.phone = phone
            client.save()
            logger.info("Repository clientes - Cliente %s actualizado", client_id)
            return client
        except Client.DoesNotExist:
            logger.warning("Repository clientes - No se pudo actualizar cliente %s inexistente", client_id)
            return None

    def delete(self, client_id):
        """Elimina un cliente por su ID."""
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            logger.info("Repository clientes - Cliente %s eliminado", client_id)
            return True
        except Client.DoesNotExist:
            logger.warning("Repository clientes - No se pudo eliminar cliente %s inexistente", client_id)
            return False
