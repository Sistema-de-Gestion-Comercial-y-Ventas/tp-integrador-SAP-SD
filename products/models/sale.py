class Sale:
    """
    Modelo que representa una venta u operación comercial.
    IMPORTANTE: Esta clase NO hereda de django.db.models.Model
    porque en esta fase inicial los datos se almacenan en memoria usando listas de Python.
    """

    def __init__(self, sale_id, client_id, product_id, quantity, status):
        self.sale_id = sale_id          # Identificador único de la venta
        self.client_id = client_id      # Cliente asociado a la venta
        self.product_id = product_id    # Producto vendido
        self.quantity = quantity        # Cantidad vendida
        self.status = status            # Estado de la venta

    def __repr__(self):
        """Representación legible del objeto, útil para debugging."""
        return (
            f"Sale(id={self.sale_id}, client_id={self.client_id}, "
            f"product_id={self.product_id}, quantity={self.quantity}, "
            f"status={self.status})"
        )