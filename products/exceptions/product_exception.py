class ProductException(Exception):     
    """Excepción personalizada para errores del dominio de productos. Hereda de la clase base Exception de Python."""       
    
    def __init__(self, message, status_code=400):         
        super().__init__(message)         
        self.message = message         
        self.status_code = status_code   # Código HTTP del error 

class ProductNotFoundException(ProductException):     
    """Se lanza cuando no se encuentra un producto por su ID."""       
    
    def __init__(self, product_id):         
        super().__init__(             
            message=f'Producto con ID {product_id} no encontrado.',             
            status_code=404         
        ) 