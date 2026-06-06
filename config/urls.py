from django.contrib import admin 
from django.urls import path   


from products.controllers.product_controller import ProductController     


# Se crea UNA SOLA instancia del controller a nivel de módulo. Esto evita crear una nueva instancia en cada petición HTTP. 
controller = ProductController()   

urlpatterns = [     
    # Panel de administración de Django (viene por defecto)     
    path('admin/', admin.site.urls), 
    
    # Endpoint: GET /products/     
    # Cuando el cliente acceda a /products/, Django llama a controller.get_products()     
    path('products/', controller.get_products), 
] 