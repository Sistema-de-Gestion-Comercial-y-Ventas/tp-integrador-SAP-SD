class ProductDTO:
    """Data Transfer Object para el producto. Define exactamente que campos se exponen al cliente."""

    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = float(price)

    def to_dict(self):
        """Convierte el DTO a un diccionario Python. Los diccionarios son facilmente serializables a JSON por Django."""
        return {
            'id': self.product_id,
            'name': self.name,
            'price': self.price,
        } 