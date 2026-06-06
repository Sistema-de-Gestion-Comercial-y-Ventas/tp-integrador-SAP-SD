from products.repositories.product_repository import ProductRepository 

class ProductService:     
    """Servicio de productos. Contiene la lógica de negocio y coordina el acceso a datos a través del Repository."""     
    def __init__(self):         
        # Se crea una instancia del Repository al inicializar el Service.         
        self.repository = ProductRepository()       
        
    def get_products(self):         
        """Obtiene la lista completa de productos. En el futuro, aquí podrías aplicar filtros, ordenamiento, paginación, descuentos automáticos, etc."""         
        return self.repository.find_all()       
    
    def get_product_by_id(self, product_id):         
        """Obtiene un producto específico por su ID."""         
        return self.repository.find_by_id(product_id) 