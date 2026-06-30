from products.models.client import Client
from products.repositories.client_repository import ClientRepository
from products.validators.client_validator import ClientValidator


class ClientService:
    """
    Servicio de clientes.
    Contiene la lógica de negocio y coordina el acceso a datos a través del Repository.
    """

    def __init__(self):
        self.repository = ClientRepository()
        self.validator = ClientValidator()

    def get_clients(self):
        """Obtiene la lista completa de clientes."""
        return self.repository.find_all()

    def get_client_by_id(self, client_id):
        """Obtiene un cliente específico por su ID."""
        return self.repository.find_by_id(client_id)

    def create_client(self, client_id, name, email, phone):
        """Crea un nuevo cliente validando sus datos."""
        self.validator.validate_name(name)
        self.validator.validate_email(email)
        self.validator.validate_phone(phone)

        client = Client(client_id, name, email, phone)
        return self.repository.create(client)

    def update_client(self, client_id, name, email, phone):
        """Actualiza un cliente existente validando sus datos."""
        self.validator.validate_name(name)
        self.validator.validate_email(email)
        self.validator.validate_phone(phone)

        return self.repository.update(client_id, name, email, phone)

    def delete_client(self, client_id):
        """Elimina un cliente por su ID."""
        return self.repository.delete(client_id)