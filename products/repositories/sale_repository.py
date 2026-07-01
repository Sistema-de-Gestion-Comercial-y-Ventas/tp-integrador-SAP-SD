import logging

from products.models.sale import Sale

logger = logging.getLogger(__name__)


class SaleRepository:
    """
    Repositorio de ventas usando Django ORM.
    Consulta a PostgreSQL a traves del ORM de Django.
    """

    def find_all(self):
        """Devuelve todas las ventas registradas."""
        logger.info("Repository ventas - Consultando todas las ventas")
        return Sale.objects.all().order_by('id')

    def find_by_id(self, sale_id):
        """Busca una venta por su ID. Devuelve None si no existe."""
        try:
            return Sale.objects.get(id=sale_id)
        except Sale.DoesNotExist:
            logger.warning("Repository ventas - Venta con ID %s no encontrada", sale_id)
            return None

    def create(self, client_id, product_id, quantity, status='pending'):
        """Crea una nueva venta."""
        sale = Sale.objects.create(
            client_id=client_id,
            product_id=product_id,
            quantity=quantity,
            status=status
        )
        logger.info("Repository ventas - Venta %s creada", sale.id)
        return sale

    def update(self, sale_id, quantity, status):
        """Actualiza los datos de una venta existente."""
        try:
            sale = Sale.objects.get(id=sale_id)
            sale.quantity = quantity
            sale.status = status
            sale.save()
            logger.info("Repository ventas - Venta %s actualizada", sale_id)
            return sale
        except Sale.DoesNotExist:
            logger.warning("Repository ventas - No se pudo actualizar venta %s inexistente", sale_id)
            return None

    def delete(self, sale_id):
        """Elimina una venta por su ID."""
        try:
            sale = Sale.objects.get(id=sale_id)
            sale.delete()
            logger.info("Repository ventas - Venta %s eliminada", sale_id)
            return True
        except Sale.DoesNotExist:
            logger.warning("Repository ventas - No se pudo eliminar venta %s inexistente", sale_id)
            return False
