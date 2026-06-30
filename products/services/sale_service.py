from products.repositories.sale_repository import SaleRepository
from products.repositories.product_repository import ProductRepository
from products.dto.sale_dto import SaleDTO


class SaleService:
    """
    Servicio de ventas.
    Contiene la lógica de negocio y coordina el acceso a datos.
    """

    def __init__(self):
        self.sale_repository = SaleRepository()
        self.product_repository = ProductRepository()

    def get_sales(self):
        """Obtiene la lista completa de ventas con el total calculado."""
        sales = self.sale_repository.find_all()

        data = []

        for sale in sales:
            product = self.product_repository.find_by_id(sale.product_id)

            total = 0
            if product is not None:
                total = product.price * sale.quantity

            data.append(
                SaleDTO(
                    sale.id,
                    sale.client_id,
                    sale.product_id,
                    sale.quantity,
                    sale.status,
                    total
                )
            )

        return data

    def get_sale_by_id(self, sale_id):
        """Obtiene una venta específica por su ID con el total calculado."""
        sale = self.sale_repository.find_by_id(sale_id)

        if sale is None:
            return None

        product = self.product_repository.find_by_id(sale.product_id)

        total = 0
        if product is not None:
            total = product.price * sale.quantity

        return SaleDTO(
            sale.id,
            sale.client_id,
            sale.product_id,
            sale.quantity,
            sale.status,
            total
        )