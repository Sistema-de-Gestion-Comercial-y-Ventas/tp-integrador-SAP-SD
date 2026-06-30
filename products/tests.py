import json

from django.test import Client, TestCase, override_settings

from products.models.product import Product
from products.repositories.product_repository import ProductRepository


@override_settings(ALLOWED_HOSTS=['localhost', 'testserver'])
class ProductApiTests(TestCase):
    """Pruebas basicas para el ABM de productos."""

    def setUp(self):
        self.client = Client(SERVER_NAME='localhost')
        ProductRepository.products = [
            Product(1, 'Mouse Gamer', 15000),
            Product(2, 'Teclado Mecanico', 45000),
            Product(3, 'Smart Watch', 120000),
        ]

    def test_product_crud_flow(self):
        create_response = self.client.post(
            '/products/',
            data=json.dumps({'name': 'Monitor LED', 'price': 90000}),
            content_type='application/json',
        )

        self.assertEqual(create_response.status_code, 201)
        created_product = create_response.json()
        self.assertEqual(created_product['name'], 'Monitor LED')
        self.assertEqual(created_product['price'], 90000)

        product_id = created_product['id']
        update_response = self.client.put(
            f'/products/{product_id}/',
            data=json.dumps({'name': 'Monitor LED 24', 'price': 110000}),
            content_type='application/json',
        )

        self.assertEqual(update_response.status_code, 200)
        updated_product = update_response.json()
        self.assertEqual(updated_product['name'], 'Monitor LED 24')
        self.assertEqual(updated_product['price'], 110000)

        delete_response = self.client.delete(f'/products/{product_id}/')

        self.assertEqual(delete_response.status_code, 200)

        get_deleted_response = self.client.get(f'/products/{product_id}/')

        self.assertEqual(get_deleted_response.status_code, 404)
