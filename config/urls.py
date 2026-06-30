from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from products.controllers.product_controller import ProductController
from products.controllers.client_controller import ClientController


# Se crea UNA SOLA instancia del controller a nivel de módulo. Esto evita crear una nueva instancia en cada petición HTTP.
controller = ProductController()
client_controller = ClientController()

urlpatterns = [
    # Panel de administración de Django (viene por defecto)
    path('admin/', admin.site.urls),

    # Endpoint: GET /products/
    path('products/', csrf_exempt(controller.products)),
    path('products/<int:product_id>/', csrf_exempt(controller.product_detail)),

    path('clients/', client_controller.get_clients),
]
