from pydantic import BaseModel


class ProductCreateSchema(BaseModel):
    name: str
    price: float


class ProductUpdateSchema(BaseModel):
    name: str
    price: float


class ProductSchema(ProductCreateSchema):
    """Esquema de respuesta para productos en FastAPI."""

    id: int


class ClientCreateSchema(BaseModel):
    id: int | None = None
    name: str
    email: str
    phone: str


class ClientUpdateSchema(BaseModel):
    name: str
    email: str
    phone: str


class ClientSchema(ClientUpdateSchema):
    """Esquema de respuesta para clientes en FastAPI."""

    id: int


class SaleCreateSchema(BaseModel):
    client_id: int
    product_id: int
    quantity: int
    status: str = "pending"


class SaleUpdateSchema(BaseModel):
    quantity: int
    status: str


class SaleSchema(BaseModel):
    """Esquema de respuesta para ventas en FastAPI."""

    id: int
    client_id: int
    product_id: int
    quantity: int
    status: str
    total: float
