class ClientDTO:
    """Data Transfer Object para clientes."""

    def __init__(self, client_id, name, email, phone):
        self.client_id = client_id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        return {
            'id': self.client_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
        }