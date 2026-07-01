import logging

from products.repositories.sale_repository import SaleRepository
from products.repositories.product_repository import ProductRepository
from products.repositories.client_repository import ClientRepository
from products.dto.sale_dto import SaleDTO
from products.exceptions.sale_exception import InvalidSaleException, SaleNotFoundException
from products.validators.sale_validator import SaleValidator

logger = logging.getLogger(__name__)


class SaleService:
    """
    Servicio de ventas.
    Contiene la logica de negocio y coordina el acceso a datos.
    """

    def __init__(self):
        self.sale_repository = SaleRepository()
        self.product_repository = ProductRepository()
        self.client_repository = ClientRepository()
        self.validator = SaleValidator()

    def get_sales(self):
        """Obtiene la lista completa de ventas con el total calculado."""
        logger.info("Service ventas - Obteniendo ventas")
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
        """Obtiene una venta especifica por su ID con el total calculado."""
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
    
    def create_sale(self, client_id, product_id, quantity, status='pending'):
        """Crea una venta y devuelve el DTO con el total calculado."""
        logger.info("Service ventas - Creando venta cliente=%s producto=%s", client_id, product_id)
        self._validate_sale_data(client_id, product_id, quantity, status)
        sale = self.sale_repository.create(client_id, product_id, quantity, status)

        return self._to_dto(sale)

    def update_sale(self, sale_id, quantity, status):
        """Actualiza una venta existente y devuelve el DTO con el total calculado."""
        sale = self.sale_repository.find_by_id(sale_id)

        if sale is None:
            logger.warning("Service ventas - Venta %s no encontrada para actualizar", sale_id)
            raise SaleNotFoundException(sale_id)

        self._validate_sale_data(sale.client_id, sale.product_id, quantity, status)
        logger.info("Service ventas - Actualizando venta %s", sale_id)
        updated_sale = self.sale_repository.update(sale_id, quantity, status)
        return self._to_dto(updated_sale)

    def delete_sale(self, sale_id):
        """Elimina una venta existente."""
        deleted = self.sale_repository.delete(sale_id)

        if not deleted:
            logger.warning("Service ventas - Venta %s no encontrada para eliminar", sale_id)
            raise SaleNotFoundException(sale_id)

        logger.info("Service ventas - Venta %s eliminada", sale_id)
        return True

    def _validate_sale_data(self, client_id, product_id, quantity, status):
        """Valida datos de venta y relaciones con cliente/producto."""
        try:
            self.validator.validate_sale_data(client_id, product_id, quantity, status)
        except ValueError as error:
            raise InvalidSaleException(str(error)) from error

        if self.client_repository.find_by_id(client_id) is None:
            raise InvalidSaleException(f'Cliente con ID {client_id} no encontrado.')

        if self.product_repository.find_by_id(product_id) is None:
            raise InvalidSaleException(f'Producto con ID {product_id} no encontrado.')

    def _to_dto(self, sale):
        """Convierte una venta del modelo a DTO calculando el total."""
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
