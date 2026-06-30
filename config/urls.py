from django.contrib import admin
from django.urls import path


from products.controllers.product_controller import ProductController
from products.controllers.client_controller import ClientController
from products.controllers.sale_controller import SaleController


# Se crea UNA SOLA instancia del controller a nivel de módulo. Esto evita crear una nueva instancia en cada petición HTTP.
controller = ProductController()
client_controller = ClientController()
sale_controller = SaleController()

urlpatterns = [
    # Panel de administración de Django (viene por defecto)
    path('admin/', admin.site.urls),

    # Endpoint: GET /products/
    path('products/', controller.get_products),
    path('products/<int:product_id>/', controller.get_product_by_id),

    path('clients/', client_controller.get_clients),

    path('sales/', sale_controller.get_sales),
    path('sales/<int:sale_id>/', sale_controller.get_sale_by_id),
]
