class ClientException(Exception):
    """Excepción base para errores de clientes."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ClientNotFoundException(ClientException):
    """Se lanza cuando no se encuentra un cliente."""

    def __init__(self, client_id):
        super().__init__(
            message=f'Cliente con ID {client_id} no encontrado.',
            status_code=404
        )


class ClientAlreadyExistsException(ClientException):
    """Se lanza cuando ya existe un cliente con el mismo ID."""

    def __init__(self, client_id):
        super().__init__(
            message=f'Ya existe un cliente con ID {client_id}.',
            status_code=409
        )