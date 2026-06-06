from products.models.product import Product 


class ProductRepository:
    """
    Repositorio de productos.
    Simula una base de datos usando una lista de objetos en memoria.
    En clases futuras, aqui se usarán consultas a PostgreSQL.
    """
    # Lista de clase: compartida por todas las instancias del Repository.
    # Actúa como nuestra 'base de datos' temporal.
    products = [
        Product(1, 'Mouse Gamer', 15000),
        Product(2, 'Teclado Mecanico', 45000),
        Product(3, 'Smart Watch', 120000),
    ]

    def find_all(self):
        """Devuelve todos los productos disponibles."""
        return self.products
    
    def find_by_id(self, product_id):
        """Busca un producto por su ID. Devuelve None si no existe."""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None