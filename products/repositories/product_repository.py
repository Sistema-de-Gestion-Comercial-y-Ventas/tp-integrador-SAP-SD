from products.models.product import Product


class ProductRepository:
    """
    Repositorio de productos.
    Simula una base de datos usando una lista de objetos en memoria.
    En clases futuras, aqui se usaran consultas a PostgreSQL.
    """

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

    def find_by_name(self, name):
        """Busca un producto por nombre. Devuelve None si no existe."""
        normalized_name = name.strip().lower()

        for product in self.products:
            if product.name.strip().lower() == normalized_name:
                return product

        return None

    def save(self, name, price):
        """Agrega un producto nuevo a la lista en memoria."""
        product = Product(self._get_next_id(), name, price)
        self.products.append(product)
        return product

    def update(self, product_id, name, price):
        """Actualiza un producto existente."""
        product = self.find_by_id(product_id)

        if product is None:
            return None

        product.name = name
        product.price = price
        return product

    def delete(self, product_id):
        """Elimina un producto por ID. Devuelve True si lo elimina."""
        product = self.find_by_id(product_id)

        if product is None:
            return False

        self.products.remove(product)
        return True

    def _get_next_id(self):
        """Calcula el proximo ID disponible."""
        if not self.products:
            return 1

        return max(product.product_id for product in self.products) + 1
