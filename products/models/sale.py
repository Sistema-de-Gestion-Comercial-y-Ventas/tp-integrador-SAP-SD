from django.db import models
from products.models.client import Client
from products.models.product import Product


class Sale(models.Model):
    """
    Modelo Django que representa una venta u operación comercial.
    Almacenado en PostgreSQL.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sales'
        ordering = ['-created_at']

    def __str__(self):
        return f"Sale(id={self.id}, client_id={self.client_id}, product_id={self.product_id}, quantity={self.quantity}, status={self.status})"

    def __repr__(self):
        return self.__str__()