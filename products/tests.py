import json

from django.test import Client as DjangoClient, TestCase

from products.models.client import Client
from products.models.product import Product
from products.models.sale import Sale
from products.services.client_service import ClientService
from products.services.product_service import ProductService


class ProductServiceTests(TestCase):

    def setUp(self):
        # Crear productos de prueba en la base de datos
        Product.objects.create(name="Mouse Gamer", price=15000)
        Product.objects.create(name="Teclado Mecanico", price=45000)
        Product.objects.create(name="Smart Watch", price=120000)
        self.service = ProductService()

    def test_get_products_returns_the_existing_products(self):
        products = self.service.get_products()

        self.assertEqual(products.count(), 3)
        self.assertEqual(products[0].name, "Mouse Gamer")

    def test_get_product_by_id_returns_the_requested_product(self):
        product = self.service.get_product_by_id(2)

        self.assertEqual(product.name, "Teclado Mecanico")
        self.assertEqual(product.price, 45000)

    def test_create_product(self):
        product = self.service.create_product("Monitor 27", 180000)

        self.assertEqual(product.name, "Monitor 27")
        self.assertEqual(product.price, 180000)
        self.assertIsNotNone(product.id)

    def test_update_product(self):
        product = self.service.update_product(2, "Teclado Profesional", 55000)

        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Teclado Profesional")
        self.assertEqual(product.price, 55000)

    def test_delete_product(self):
        deleted = self.service.delete_product(3)

        self.assertTrue(deleted)
        self.assertIsNone(self.service.get_product_by_id(3))


class ClientServiceTests(TestCase):

    def setUp(self):
        # Crear clientes de prueba en la base de datos
        Client.objects.create(name="Juan Pérez", email="juan.perez@gmail.com", phone="1122334455")
        Client.objects.create(name="María Gómez", email="maria.gomez@gmail.com", phone="1166778899")
        Client.objects.create(name="Carlos López", email="carlos.lopez@gmail.com", phone="1199887766")
        self.service = ClientService()

    def test_create_client(self):
        client = self.service.create_client(10, "Ana Garcia", "ana.garcia@mail.com", "1122334455")

        self.assertEqual(client.name, "Ana Garcia")
        self.assertEqual(client.email, "ana.garcia@mail.com")
        self.assertIsNotNone(client.id)

    def test_update_client(self):
        client = self.service.update_client(2, "Maria Actualizada", "maria.actualizada@mail.com", "1188997766")

        self.assertIsNotNone(client)
        self.assertEqual(client.name, "Maria Actualizada")
        self.assertEqual(client.email, "maria.actualizada@mail.com")

    def test_delete_client(self):
        deleted = self.service.delete_client(3)

        self.assertTrue(deleted)
        self.assertIsNone(self.service.get_client_by_id(3))

    def test_create_client_with_invalid_email_raises_error(self):
        with self.assertRaises(ValueError):
            self.service.create_client(10, "Ana Garcia", "email-invalido", "1122334455")


class ClientControllerTests(TestCase):

    def setUp(self):
        # Crear clientes de prueba en la base de datos
        Client.objects.create(name="Juan Pérez", email="juan.perez@gmail.com", phone="1122334455")
        Client.objects.create(name="María Gómez", email="maria.gomez@gmail.com", phone="1166778899")
        Client.objects.create(name="Carlos López", email="carlos.lopez@gmail.com", phone="1199887766")
        self.client = DjangoClient()

    def test_get_clients_via_api(self):
        response = self.client.get("/clients/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Juan Pérez")

    def test_get_client_by_id_via_api(self):
        response = self.client.get("/clients/2/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "María Gómez")

    def test_create_client_via_api(self):
        response = self.client.post(
            "/clients/",
            data='{"id": 10, "name": "Ana Garcia", "email": "ana.garcia@mail.com", "phone": "1122334455"}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Ana Garcia")

    def test_update_client_via_api(self):
        response = self.client.put(
            "/clients/2/",
            data='{"name": "Maria Actualizada", "email": "maria.actualizada@mail.com", "phone": "1188997766"}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Maria Actualizada")

    def test_delete_client_via_api(self):
        response = self.client.delete("/clients/3/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Cliente eliminado correctamente.")


class ProductControllerTests(TestCase):

    def setUp(self):
        # Crear productos de prueba en la base de datos
        Product.objects.create(name="Mouse Gamer", price=15000)
        Product.objects.create(name="Teclado Mecanico", price=45000)
        Product.objects.create(name="Smart Watch", price=120000)
        self.client = DjangoClient()

    def test_get_products_via_api(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Mouse Gamer")

    def test_get_product_by_id_via_api(self):
        response = self.client.get("/products/2/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Teclado Mecanico")

    def test_create_product_via_public_api(self):
        response = self.client.post(
            "/products/",
            data=json.dumps({"name": "Monitor LED", "price": 90000}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json()["id"])
        self.assertEqual(response.json()["name"], "Monitor LED")

    def test_update_product_via_public_api(self):
        created = self.client.post(
            "/products/",
            data=json.dumps({"name": "Monitor LED", "price": 90000}),
            content_type="application/json"
        )
        product_id = created.json()["id"]

        response = self.client.put(
            f"/products/{product_id}/",
            data=json.dumps({"name": "Monitor LED 24", "price": 110000}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Monitor LED 24")

    def test_delete_product_via_public_api(self):
        created = self.client.post(
            "/products/",
            data=json.dumps({"name": "Monitor LED", "price": 90000}),
            content_type="application/json"
        )
        product_id = created.json()["id"]

        response = self.client.delete(f"/products/{product_id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(f"/products/{product_id}/").status_code, 404)

    def test_admin_create_product_via_api(self):
        response = self.client.post(
            "/admin/products/",
            data='{"id": 10, "name": "Auriculares", "price": 65000}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Auriculares")

    def test_admin_update_product_via_api(self):
        response = self.client.put(
            "/admin/products/2/",
            data='{"name": "Teclado Profesional", "price": 55000}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Teclado Profesional")

    def test_admin_delete_product_via_api(self):
        response = self.client.delete("/admin/products/3/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Producto eliminado correctamente.")
