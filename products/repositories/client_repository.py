from products.exceptions.client_exception import ClientAlreadyExistsException
from products.models.client import Client


class ClientRepository:
    """
    Repositorio de clientes.
    Simula una base de datos usando una lista de objetos en memoria.
    """

    _initial_clients_data = [
        (1, "Juan Pérez", "juan.perez@gmail.com", "1122334455"),
        (2, "María Gómez", "maria.gomez@gmail.com", "1166778899"),
        (3, "Carlos López", "carlos.lopez@gmail.com", "1199887766"),
    ]
    clients = [Client(*data) for data in _initial_clients_data]

    @classmethod
    def reset_data(cls):
        """Restablece la lista de clientes a su estado inicial."""
        cls.clients = [Client(*data) for data in cls._initial_clients_data]

    def find_all(self):
        """Devuelve todos los clientes registrados."""
        return self.clients

    def find_by_id(self, client_id):
        """Busca un cliente por su ID. Devuelve None si no existe."""
        for client in self.clients:
            if client.client_id == client_id:
                return client

        return None

    def create(self, client):
        """Agrega un nuevo cliente a la lista en memoria."""
        if self.find_by_id(client.client_id) is not None:
            raise ClientAlreadyExistsException(client.client_id)

        self.clients.append(client)
        return client

    def update(self, client_id, name, email, phone):
        """Actualiza los datos de un cliente existente."""
        client = self.find_by_id(client_id)
        if client is None:
            return None

        client.name = name
        client.email = email
        client.phone = phone
        return client

    def delete(self, client_id):
        """Elimina un cliente por su ID."""
        client = self.find_by_id(client_id)
        if client is None:
            return False

        self.clients.remove(client)
        return True