class SaleDTO:
    """
    Data Transfer Object para ventas.
    Define que datos de una venta se exponen en la respuesta JSON.
    """

    def __init__(self, sale_id, client_id, product_id, quantity, status, total):
        self.sale_id = sale_id
        self.client_id = client_id
        self.product_id = product_id
        self.quantity = quantity
        self.status = status
        self.total = float(total)

    def to_dict(self):
        """Convierte el DTO a un diccionario serializable a JSON."""
        return {
            'id': self.sale_id,
            'client_id': self.client_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'status': self.status,
            'total': self.total,
        }
