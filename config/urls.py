from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from products.controllers.client_controller import ClientController
from products.controllers.product_controller import ProductController
from products.controllers.sale_controller import SaleController


# Se crea UNA SOLA instancia de cada controller a nivel de modulo.
product_controller = ProductController()
client_controller = ClientController()
sale_controller = SaleController()

urlpatterns = [
    # Endpoints publicos de productos
    path('products/', csrf_exempt(product_controller.products)),
    path('products/<int:product_id>/', csrf_exempt(product_controller.product_detail)),

    # Endpoints administrativos de productos
    path('admin/products/', csrf_exempt(product_controller.create_product)),
    path('admin/products/<int:product_id>/', csrf_exempt(product_controller.admin_product_detail)),

    # Panel de administracion de Django (viene por defecto)
    path('admin/', admin.site.urls),

    # Endpoints publicos de clientes
    path('clients/', csrf_exempt(client_controller.client_collection)),
    path('clients/<int:client_id>/', csrf_exempt(client_controller.client_detail)),

    # Endpoints de ventas
    path('sales/', csrf_exempt(sale_controller.sale_collection)),
    path('sales/<int:sale_id>/', csrf_exempt(sale_controller.sale_detail)),
]
