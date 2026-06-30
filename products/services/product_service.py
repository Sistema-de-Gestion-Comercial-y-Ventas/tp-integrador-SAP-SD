from products.models.product import Product
from products.repositories.product_repository import ProductRepository
from products.validators.product_validator import ProductValidator


class ProductService:
    """Servicio de productos. Contiene la lógica de negocio y coordina el acceso a datos a través del Repository."""

    def __init__(self):
        self.repository = ProductRepository()
        self.validator = ProductValidator()

    def get_products(self):
        """Obtiene la lista completa de productos."""
        return self.repository.find_all()

    def get_product_by_id(self, product_id):
        """Obtiene un producto específico por su ID."""
        return self.repository.find_by_id(product_id)

    def create_product(self, product_id, name, price):
        """Crea un nuevo producto validando sus datos."""
        self.validator.validate_name(name)
        self.validator.validate_price(price)

        product = Product(product_id, name, price)
        return self.repository.create(product)

    def update_product(self, product_id, name, price):
        """Actualiza un producto existente validando sus datos."""
        self.validator.validate_name(name)
        self.validator.validate_price(price)

        return self.repository.update(product_id, name, price)

    def delete_product(self, product_id):
        """Elimina un producto por su ID."""
        return self.repository.delete(product_id) 