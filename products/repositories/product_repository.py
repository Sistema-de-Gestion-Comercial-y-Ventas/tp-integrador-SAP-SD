from products.models.product import Product 


class ProductRepository:
    """
    Repositorio de productos.
    Simula una base de datos usando una lista de objetos en memoria.
    En clases futuras, aqui se usarán consultas a PostgreSQL.
    """
    # Datos iniciales para crear productos nuevos cada vez.
    _initial_products_data = [
        (1, 'Mouse Gamer', 15000),
        (2, 'Teclado Mecanico', 45000),
        (3, 'Smart Watch', 120000),
    ]
    products = [Product(*data) for data in _initial_products_data]

    @classmethod
    def reset_data(cls):
        """Restablece la lista de productos a su estado inicial."""
        cls.products = [Product(*data) for data in cls._initial_products_data]

    def find_all(self):
        """Devuelve todos los productos disponibles."""
        return self.products
    
    def find_by_id(self, product_id):
        """Busca un producto por su ID. Devuelve None si no existe."""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def create(self, product):
        """Agrega un nuevo producto a la lista en memoria."""
        if self.find_by_id(product.product_id) is not None:
            raise ValueError(f'Ya existe un producto con ID {product.product_id}.')

        self.products.append(product)
        return product

    def update(self, product_id, name, price):
        """Actualiza los datos de un producto existente."""
        product = self.find_by_id(product_id)
        if product is None:
            return None

        product.name = name
        product.price = price
        return product

    def delete(self, product_id):
        """Elimina un producto por su ID."""
        product = self.find_by_id(product_id)
        if product is None:
            return False

        self.products.remove(product)
        return True