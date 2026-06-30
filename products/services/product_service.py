from products.exceptions.product_exception import (
    ProductAlreadyExistsException,
    ProductNotFoundException,
    ProductValidationException,
)
from products.repositories.product_repository import ProductRepository
from products.validators.product_validator import ProductValidator


class ProductService:
    """Servicio de productos. Contiene la logica de negocio."""

    def __init__(self):
        self.repository = ProductRepository()
        self.validator = ProductValidator()

    def get_products(self):
        """Obtiene la lista completa de productos."""
        return self.repository.find_all()

    def get_product_by_id(self, product_id):
        """Obtiene un producto especifico por su ID."""
        return self.repository.find_by_id(product_id)

    def create_product(self, name, price):
        """Crea un producto nuevo luego de validar sus datos."""
        self._validate_product_data(name, price)

        if self.repository.find_by_name(name) is not None:
            raise ProductAlreadyExistsException(name)

        return self.repository.save(name.strip(), price)

    def update_product(self, product_id, name, price):
        """Actualiza un producto existente."""
        product = self.repository.find_by_id(product_id)

        if product is None:
            raise ProductNotFoundException(product_id)

        self._validate_product_data(name, price)

        product_with_same_name = self.repository.find_by_name(name)
        if (
            product_with_same_name is not None
            and product_with_same_name.product_id != product_id
        ):
            raise ProductAlreadyExistsException(name)

        return self.repository.update(product_id, name.strip(), price)

    def delete_product(self, product_id):
        """Elimina un producto existente."""
        deleted = self.repository.delete(product_id)

        if not deleted:
            raise ProductNotFoundException(product_id)

    def _validate_product_data(self, name, price):
        """Centraliza las validaciones del producto."""
        try:
            self.validator.validate_name(name)
            self.validator.validate_price(price)
        except ValueError as error:
            raise ProductValidationException(str(error)) from error
