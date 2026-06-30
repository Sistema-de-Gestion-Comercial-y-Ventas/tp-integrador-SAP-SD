from django.db import models


class Product(models.Model):
    """
    Modelo Django que representa un producto del catálogo.
    Almacenado en PostgreSQL.
    """
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return f'Product(id={self.id}, name={self.name}, price={self.price})'

    def __repr__(self):
        return self.__str__()