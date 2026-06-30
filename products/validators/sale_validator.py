class SaleValidator:
    """Validador de datos para ventas."""

    VALID_STATUSES = ["pendiente", "confirmada", "cancelada"]

    def validate_quantity(self, quantity):
        """Valida que la cantidad vendida sea un número entero mayor a cero."""
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("La cantidad debe ser un número entero mayor a cero.")

    def validate_status(self, status):
        """Valida que el estado de la venta sea uno de los permitidos."""
        if status not in self.VALID_STATUSES:
            raise ValueError("El estado de la venta no es válido.")

    def validate_sale_data(self, client_id, product_id, quantity, status):
        """Valida los datos principales de una venta."""
        if not client_id:
            raise ValueError("El cliente es obligatorio.")

        if not product_id:
            raise ValueError("El producto es obligatorio.")

        self.validate_quantity(quantity)
        self.validate_status(status)