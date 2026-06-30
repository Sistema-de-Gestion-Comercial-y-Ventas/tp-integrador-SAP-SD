from django.contrib import admin
from django.urls import path

from products.controllers.client_controller import ClientController
from products.controllers.product_controller import ProductController


# Se crea UNA SOLA instancia del controller a nivel de módulo. Esto evita crear una nueva instancia en cada petición HTTP.
product_controller = ProductController()
client_controller = ClientController()

urlpatterns = [
    # Endpoints de administración de productos
    path('admin/products/', product_controller.create_product),
    path('admin/products/<int:product_id>/', product_controller.admin_product_detail),

    # Panel de administración de Django (viene por defecto)
    path('admin/', admin.site.urls),

    # Endpoints públicos de productos
    path('products/', product_controller.get_products),
    path('products/<int:product_id>/', product_controller.get_product_by_id),

    # Endpoints públicos de clientes
    path('clients/', client_controller.client_collection),
    path('clients/<int:client_id>/', client_controller.client_detail),
]
