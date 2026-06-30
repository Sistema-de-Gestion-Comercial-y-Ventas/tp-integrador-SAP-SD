from pydantic import BaseModel


class ProductSchema(BaseModel):
    """Esquema de respuesta para productos en FastAPI."""

    id: int
    name: str
    price: float


class ClientSchema(BaseModel):
    """Esquema de respuesta para clientes en FastAPI."""

    id: int
    name: str
    email: str
    phone: str


class SaleSchema(BaseModel):
    """Esquema de respuesta para ventas en FastAPI."""

    id: int
    client_id: int
    product_id: int
    quantity: int
    status: str
    total: float