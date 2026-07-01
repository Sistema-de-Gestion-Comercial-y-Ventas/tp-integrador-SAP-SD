class ClientValidator:
    """Validador de datos para clientes."""

    def validate_name(self, name):
        if not name or len(name.strip()) < 3:
            raise ValueError('El nombre del cliente debe tener al menos 3 caracteres.')

    def validate_email(self, email):
        if not email or '@' not in email:
            raise ValueError('El email no es valido.')

    def validate_phone(self, phone):
        if not phone or len(str(phone).strip()) < 7:
            raise ValueError('El telefono debe tener al menos 7 digitos.')