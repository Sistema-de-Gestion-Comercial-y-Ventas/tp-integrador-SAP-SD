class Client:
    """
    Modelo que representa un cliente del sistema comercial.
    IMPORTANTE: Esta clase NO hereda de django.db.models.Model
    porque en esta fase inicial los datos se almacenan en memoria usando listas de Python.
    """

    def __init__(self, client_id, name, email, phone):
        self.client_id = client_id      # Identificador único del cliente
        self.name = name                # Nombre del cliente
        self.email = email              # Correo electrónico
        self.phone = phone              # Teléfono de contacto

    def __repr__(self):
        """Representación legible del objeto, útil para debugging."""
        return f"Client(id={self.client_id}, name={self.name}, email={self.email}, phone={self.phone})"