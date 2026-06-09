class ClientValidator:
    """Validador de datos para clientes."""

    def validate_name(self, name):
        if not name or len(name.strip()) < 3:
            raise ValueError('El nombre del cliente debe tener al menos 3 caracteres.')

    def validate_email(self, email):
        if not email or '@' not in email:
            raise ValueError('El email no es válido.')