from products.models.product import Product


class ProductRepository:
    """
    Repositorio de productos usando Django ORM.
    Consulta a PostgreSQL a través del ORM de Django.
    """

    def find_all(self):
        """Devuelve todos los productos disponibles."""
        return Product.objects.all().order_by('id')

    def find_by_id(self, product_id):
        """Busca un producto por su ID. Devuelve None si no existe."""
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def find_by_name(self, name):
        """Busca un producto por nombre. Devuelve None si no existe."""
        try:
            return Product.objects.get(name__iexact=name)
        except Product.DoesNotExist:
            return None

    def create(self, name, price):
        """Crea un nuevo producto."""
        product = Product.objects.create(name=name, price=price)
        return product

    def update(self, product_id, name, price):
        """Actualiza los datos de un producto existente."""
        try:
            product = Product.objects.get(id=product_id)
            product.name = name
            product.price = price
            product.save()
            return product
        except Product.DoesNotExist:
            return None

    def delete(self, product_id):
        """Elimina un producto por su ID."""
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return True
        except Product.DoesNotExist:
            return False
