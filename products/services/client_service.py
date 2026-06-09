from products.repositories.client_repository import ClientRepository


class ClientService:
    """
    Servicio de clientes.
    Contiene la lógica de negocio y coordina el acceso a datos a través del Repository.
    """

    def __init__(self):
        self.repository = ClientRepository()

    def get_clients(self):
        """Obtiene la lista completa de clientes."""
        return self.repository.find_all()

    def get_client_by_id(self, client_id):
        """Obtiene un cliente específico por su ID."""
        return self.repository.find_by_id(client_id)