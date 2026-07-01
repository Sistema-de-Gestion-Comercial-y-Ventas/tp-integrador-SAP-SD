from fastapi import APIRouter, HTTPException

from products.exceptions.client_exception import ClientException, ClientNotFoundException
from products.exceptions.product_exception import ProductException, ProductNotFoundException
from products.exceptions.sale_exception import SaleException, SaleNotFoundException
from products.services.client_service import ClientService
from products.services.product_service import ProductService
from products.services.sale_service import SaleService

from fastapi_app.schemas import (
    ClientCreateSchema,
    ClientUpdateSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
    SaleCreateSchema,
    SaleUpdateSchema,
)


router = APIRouter()

product_service = ProductService()
client_service = ClientService()
sale_service = SaleService()


def product_to_dict(product):
    return {
        "id": product.id,
        "name": product.name,
        "price": float(product.price),
    }


def client_to_dict(client):
    return {
        "id": client.id,
        "name": client.name,
        "email": client.email,
        "phone": client.phone,
    }


def raise_http_error(error):
    status_code = getattr(error, "status_code", 400)
    message = getattr(error, "message", str(error))
    raise HTTPException(status_code=status_code, detail=message)


@router.get("/products")
def get_products():
    """Devuelve todos los productos usando la logica existente del proyecto Django."""
    return [product_to_dict(product) for product in product_service.get_products()]


@router.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    """Devuelve un producto por ID."""
    product = product_service.get_product_by_id(product_id)

    if product is None:
        raise_http_error(ProductNotFoundException(product_id))

    return product_to_dict(product)


@router.post("/products", status_code=201)
def create_product(payload: ProductCreateSchema):
    """Crea un producto."""
    try:
        product = product_service.create_product(payload.name, payload.price)
        return product_to_dict(product)
    except ProductException as error:
        raise_http_error(error)


@router.put("/products/{product_id}")
def update_product(product_id: int, payload: ProductUpdateSchema):
    """Actualiza un producto."""
    try:
        product = product_service.update_product(product_id, payload.name, payload.price)
        return product_to_dict(product)
    except ProductException as error:
        raise_http_error(error)


@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Elimina un producto."""
    try:
        product_service.delete_product(product_id)
        return {"message": "Producto eliminado correctamente."}
    except ProductException as error:
        raise_http_error(error)


@router.get("/clients")
def get_clients():
    """Devuelve todos los clientes usando la logica existente del proyecto Django."""
    return [client_to_dict(client) for client in client_service.get_clients()]


@router.get("/clients/{client_id}")
def get_client_by_id(client_id: int):
    """Devuelve un cliente por ID."""
    client = client_service.get_client_by_id(client_id)

    if client is None:
        raise_http_error(ClientNotFoundException(client_id))

    return client_to_dict(client)


@router.post("/clients", status_code=201)
def create_client(payload: ClientCreateSchema):
    """Crea un cliente."""
    try:
        client = client_service.create_client(
            payload.id,
            payload.name,
            payload.email,
            payload.phone,
        )
        return client_to_dict(client)
    except (ClientException, ValueError) as error:
        raise_http_error(error)


@router.put("/clients/{client_id}")
def update_client(client_id: int, payload: ClientUpdateSchema):
    """Actualiza un cliente."""
    try:
        client = client_service.update_client(
            client_id,
            payload.name,
            payload.email,
            payload.phone,
        )
        if client is None:
            raise ClientNotFoundException(client_id)
        return client_to_dict(client)
    except (ClientException, ValueError) as error:
        raise_http_error(error)


@router.delete("/clients/{client_id}")
def delete_client(client_id: int):
    """Elimina un cliente."""
    try:
        deleted = client_service.delete_client(client_id)
        if not deleted:
            raise ClientNotFoundException(client_id)
        return {"message": "Cliente eliminado correctamente."}
    except ClientException as error:
        raise_http_error(error)


@router.get("/sales")
def get_sales():
    """Devuelve todas las ventas usando la logica existente del proyecto Django."""
    return [sale.to_dict() for sale in sale_service.get_sales()]


@router.get("/sales/{sale_id}")
def get_sale_by_id(sale_id: int):
    """Devuelve una venta por ID."""
    sale = sale_service.get_sale_by_id(sale_id)

    if sale is None:
        raise_http_error(SaleNotFoundException(sale_id))

    return sale.to_dict()


@router.post("/sales", status_code=201)
def create_sale(payload: SaleCreateSchema):
    """Crea una venta."""
    try:
        sale = sale_service.create_sale(
            payload.client_id,
            payload.product_id,
            payload.quantity,
            payload.status,
        )
        return sale.to_dict()
    except SaleException as error:
        raise_http_error(error)


@router.put("/sales/{sale_id}")
def update_sale(sale_id: int, payload: SaleUpdateSchema):
    """Actualiza una venta."""
    try:
        sale = sale_service.update_sale(sale_id, payload.quantity, payload.status)
        return sale.to_dict()
    except SaleException as error:
        raise_http_error(error)


@router.delete("/sales/{sale_id}")
def delete_sale(sale_id: int):
    """Elimina una venta."""
    try:
        sale_service.delete_sale(sale_id)
        return {"message": "Venta eliminada correctamente."}
    except SaleException as error:
        raise_http_error(error)
