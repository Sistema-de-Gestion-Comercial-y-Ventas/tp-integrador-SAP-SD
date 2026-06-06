class Product:     
    """     
    Modelo que representa un producto del catálogo.       
    IMPORTANTE: Esta clase NO hereda de django.db.models.Model     
    porque en esta fase inicial no usamos base de datos.     
    Los datos se almacenan en memoria usando listas Python.     
    """ 

    def __init__(self, product_id, name, price):         
        self.product_id = product_id   # Identificador único del producto         
        self.name = name               # Nombre del producto         
        self.price = price             # Precio en pesos       
    
    def __repr__(self):         
        """Representación legible del objeto (útil para debugging)."""         
        return f'Product(id={self.product_id}, name={self.name}, price={self.price})'