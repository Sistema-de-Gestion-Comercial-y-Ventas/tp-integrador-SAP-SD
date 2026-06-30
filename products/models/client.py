from django.db import models


class Client(models.Model):
    """
    Modelo Django que representa un cliente del sistema comercial.
    Almacenado en PostgreSQL.
    """
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=20, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'
        ordering = ['-created_at']

    def __str__(self):
        return f"Client(id={self.id}, name={self.name}, email={self.email}, phone={self.phone})"

    def __repr__(self):
        return self.__str__()