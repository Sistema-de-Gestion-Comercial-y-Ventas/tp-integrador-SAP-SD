from products.models.sale import Sale


class SaleRepository:
    """
    Repositorio de ventas usando Django ORM.
    Consulta a PostgreSQL a través del ORM de Django.
    """

    def find_all(self):
        """Devuelve todas las ventas registradas."""
        return Sale.objects.all().order_by('id')

    def find_by_id(self, sale_id):
        """Busca una venta por su ID. Devuelve None si no existe."""
        try:
            return Sale.objects.get(id=sale_id)
        except Sale.DoesNotExist:
            return None

    def create(self, client_id, product_id, quantity, status='pending'):
        """Crea una nueva venta."""
        sale = Sale.objects.create(
            client_id=client_id,
            product_id=product_id,
            quantity=quantity,
            status=status
        )
        return sale

    def update(self, sale_id, quantity, status):
        """Actualiza los datos de una venta existente."""
        try:
            sale = Sale.objects.get(id=sale_id)
            sale.quantity = quantity
            sale.status = status
            sale.save()
            return sale
        except Sale.DoesNotExist:
            return None

    def delete(self, sale_id):
        """Elimina una venta por su ID."""
        try:
            sale = Sale.objects.get(id=sale_id)
            sale.delete()
            return True
        except Sale.DoesNotExist:
            return False