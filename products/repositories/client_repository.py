from products.exceptions.client_exception import ClientAlreadyExistsException
from products.models.client import Client


class ClientRepository:
    """
    Repositorio de clientes usando Django ORM.
    Consulta a PostgreSQL a través del ORM de Django.
    """

    def find_all(self):
        """Devuelve todos los clientes registrados."""
        return Client.objects.all().order_by('id')

    def find_by_id(self, client_id):
        """Busca un cliente por su ID. Devuelve None si no existe."""
        try:
            return Client.objects.get(id=client_id)
        except Client.DoesNotExist:
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
        return client

    def update(self, client_id, name, email, phone):
        """Actualiza los datos de un cliente existente."""
        try:
            client = Client.objects.get(id=client_id)
            client.name = name
            client.email = email
            client.phone = phone
            client.save()
            return client
        except Client.DoesNotExist:
            return None

    def delete(self, client_id):
        """Elimina un cliente por su ID."""
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            return True
        except Client.DoesNotExist:
            return False