class ProductException(Exception):
    """Excepcion personalizada para errores del dominio de productos."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ProductNotFoundException(ProductException):
    """Se lanza cuando no se encuentra un producto por su ID."""

    def __init__(self, product_id):
        super().__init__(
            message=f'Producto con ID {product_id} no encontrado.',
            status_code=404
        )


class ProductAlreadyExistsException(ProductException):
    """Se lanza cuando ya existe un producto con el mismo nombre."""

    def __init__(self, name):
        super().__init__(
            message=f'Ya existe un producto con el nombre {name}.',
            status_code=409
        )


class ProductValidationException(ProductException):
    """Se lanza cuando los datos del producto son invalidos."""

    def __init__(self, message):
        super().__init__(
            message=message,
            status_code=400
        )
