class ProductValidator:
    """Validador de datos para productos."""

    def validate_name(self, name):
        """Valida que el nombre del producto sea un texto valido."""
        if not isinstance(name, str) or len(name.strip()) < 3:
            raise ValueError('El nombre del producto debe tener al menos 3 caracteres.')

    def validate_price(self, price):
        """Valida que el precio sea un numero positivo."""
        if not isinstance(price, (int, float)) or isinstance(price, bool) or price <= 0:
            raise ValueError('El precio debe ser un numero mayor a cero.')
