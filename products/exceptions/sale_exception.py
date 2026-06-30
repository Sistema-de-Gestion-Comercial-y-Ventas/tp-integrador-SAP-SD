class SaleException(Exception):
    """Excepción base para errores del dominio de ventas."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class SaleNotFoundException(SaleException):
    """Se lanza cuando no se encuentra una venta por su ID."""

    def __init__(self, sale_id):
        super().__init__(
            message=f'Venta con ID {sale_id} no encontrada.',
            status_code=404
        )


class InvalidSaleException(SaleException):
    """Se lanza cuando una venta tiene datos inválidos."""

    def __init__(self, message):
        super().__init__(
            message=message,
            status_code=400
        )