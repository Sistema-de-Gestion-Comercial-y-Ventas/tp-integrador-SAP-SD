from products.models.client import Client


class ClientRepository:
    """
    Repositorio de clientes.
    Simula una base de datos usando una lista de objetos en memoria.
    """

    clients = [
        Client(1, "Juan Pérez", "juan.perez@gmail.com", "1122334455"),
        Client(2, "María Gómez", "maria.gomez@gmail.com", "1166778899"),
        Client(3, "Carlos López", "carlos.lopez@gmail.com", "1199887766"),
    ]

    def find_all(self):
        """Devuelve todos los clientes registrados."""
        return self.clients

    def find_by_id(self, client_id):
        """Busca un cliente por su ID. Devuelve None si no existe."""
        for client in self.clients:
            if client.client_id == client_id:
                return client

        return None