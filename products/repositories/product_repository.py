import logging

from products.models.product import Product

logger = logging.getLogger(__name__)


class ProductRepository:
    """
    Repositorio de productos usando Django ORM.
    Consulta a PostgreSQL a traves del ORM de Django.
    """

    def find_all(self):
        """Devuelve todos los productos disponibles."""
        logger.info("Repository productos - Consultando todos los productos")
        return Product.objects.all().order_by('id')

    def find_by_id(self, product_id):
        """Busca un producto por su ID. Devuelve None si no existe."""
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            logger.warning("Repository productos - Producto con ID %s no encontrado", product_id)
            return None

    def find_by_name(self, name):
        """Busca un producto por nombre. Devuelve None si no existe."""
        try:
            return Product.objects.get(name__iexact=name)
        except Product.DoesNotExist:
            return None

    def create(self, name, price):
        """Crea un nuevo producto."""
        logger.info("Repository productos - Creando producto %s", name)
        product = Product.objects.create(name=name, price=price)
        return product

    def update(self, product_id, name, price):
        """Actualiza los datos de un producto existente."""
        try:
            product = Product.objects.get(id=product_id)
            product.name = name
            product.price = price
            product.save()
            logger.info("Repository productos - Producto %s actualizado", product_id)
            return product
        except Product.DoesNotExist:
            logger.warning("Repository productos - No se pudo actualizar producto %s inexistente", product_id)
            return None

    def delete(self, product_id):
        """Elimina un producto por su ID."""
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            logger.info("Repository productos - Producto %s eliminado", product_id)
            return True
        except Product.DoesNotExist:
            logger.warning("Repository productos - No se pudo eliminar producto %s inexistente", product_id)
            return False
