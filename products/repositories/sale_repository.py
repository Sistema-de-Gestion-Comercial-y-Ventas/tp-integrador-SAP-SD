from products.models.sale import Sale


class SaleRepository:
    """
    Repositorio de ventas.
    Simula una base de datos usando una lista de objetos en memoria.
    """

    sales = [
        Sale(1, 1, 1, 2, "confirmada"),
        Sale(2, 2, 2, 1, "pendiente"),
        Sale(3, 3, 3, 1, "cancelada"),
    ]

    def find_all(self):
        """Devuelve todas las ventas registradas."""
        return self.sales

    def find_by_id(self, sale_id):
        """Busca una venta por su ID. Devuelve None si no existe."""
        for sale in self.sales:
            if sale.sale_id == sale_id:
                return sale

        return None