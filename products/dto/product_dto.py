class ProductDTO:     
    """Data Transfer Object para el producto. Define exactamente qué campos se exponen al cliente."""       
    def  __init__(self, product_id, name, price):         
        self.product_id = product_id         
        self.name = name         
        self.price = price       
    def to_dict(self):         
        """Convierte el DTO a un diccionario Python. Los diccionarios son fácilmente serializables a JSON por Django."""         
        return {             
            'id': self.product_id,             
            'name': self.name,             
            'price': self.price,
        } 