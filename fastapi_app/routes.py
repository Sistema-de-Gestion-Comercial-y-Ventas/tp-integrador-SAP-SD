from fastapi import APIRouter, HTTPException

from products.services.product_service import ProductService
from products.services.client_service import ClientService
from products.services.sale_service import SaleService


router = APIRouter()

product_service = ProductService()
client_service = ClientService()
sale_service = SaleService()


@router.get("/products")
def get_products():
    """Devuelve todos los productos usando la lógica existente del proyecto Django."""
    products = product_service.get_products()

    data = []

    for product in products:
        data.append({
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
        })

    return data


@router.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    """Devuelve un producto por ID."""
    product = product_service.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Producto con ID {product_id} no encontrado."
        )

    return {
        "id": product.product_id,
        "name": product.name,
        "price": product.price,
    }


@router.get("/clients")
def get_clients():
    """Devuelve todos los clientes usando la lógica existente del proyecto Django."""
    clients = client_service.get_clients()

    data = []

    for client in clients:
        data.append({
            "id": client.client_id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
        })

    return data


@router.get("/sales")
def get_sales():
    """Devuelve todas las ventas usando la lógica existente del proyecto Django."""
    sales = sale_service.get_sales()

    data = []

    for sale in sales:
        data.append(sale.to_dict())

    return data


@router.get("/sales/{sale_id}")
def get_sale_by_id(sale_id: int):
    """Devuelve una venta por ID."""
    sale = sale_service.get_sale_by_id(sale_id)

    if sale is None:
        raise HTTPException(
            status_code=404,
            detail=f"Venta con ID {sale_id} no encontrada."
        )

    return sale.to_dict()