import json

from django.test import Client as DjangoClient, TestCase

from products.models.client import Client
from products.models.product import Product
from products.models.sale import Sale
from products.services.client_service import ClientService
from products.services.product_service import ProductService
from products.services.sale_service import SaleService


class ProductServiceTests(TestCase):

    def setUp(self):
        # Crear productos de prueba en la base de datos
        self.mouse = Product.objects.create(name="Mouse Gamer", price=15000)
        self.keyboard = Product.objects.create(name="Teclado Mecanico", price=45000)
        self.smart_watch = Product.objects.create(name="Smart Watch", price=120000)
        self.service = ProductService()

    def test_get_products_returns_the_existing_products(self):
        products = self.service.get_products()

        self.assertEqual(products.count(), 3)
        self.assertEqual(products[0].name, "Mouse Gamer")

    def test_get_product_by_id_returns_the_requested_product(self):
        product = self.service.get_product_by_id(self.keyboard.id)

        self.assertEqual(product.name, "Teclado Mecanico")
        self.assertEqual(product.price, 45000)

    def test_create_product(self):
        product = self.service.create_product("Monitor 27", 180000)

        self.assertEqual(product.name, "Monitor 27")
        self.assertEqual(product.price, 180000)
        self.assertIsNotNone(product.id)

    def test_update_product(self):
        product = self.service.update_product(self.keyboard.id, "Teclado Profesional", 55000)

        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Teclado Profesional")
        self.assertEqual(product.price, 55000)

    def test_delete_product(self):
        deleted = self.service.delete_product(self.smart_watch.id)

        self.assertTrue(deleted)
        self.assertIsNone(self.service.get_product_by_id(self.smart_watch.id))


class ClientServiceTests(TestCase):

    def setUp(self):
        # Crear clientes de prueba en la base de datos
        self.juan = Client.objects.create(name="Juan Perez", email="juan.perez@gmail.com", phone="1122334455")
        self.maria = Client.objects.create(name="Maria Gomez", email="maria.gomez@gmail.com", phone="1166778899")
        self.carlos = Client.objects.create(name="Carlos Lopez", email="carlos.lopez@gmail.com", phone="1199887766")
        self.service = ClientService()

    def test_create_client(self):
        client = self.service.create_client(10, "Ana Garcia", "ana.garcia@mail.com", "1122334455")

        self.assertEqual(client.name, "Ana Garcia")
        self.assertEqual(client.email, "ana.garcia@mail.com")
        self.assertIsNotNone(client.id)

    def test_update_client(self):
        client = self.service.update_client(self.maria.id, "Maria Actualizada", "maria.actualizada@mail.com", "1188997766")

        self.assertIsNotNone(client)
        self.assertEqual(client.name, "Maria Actualizada")
        self.assertEqual(client.email, "maria.actualizada@mail.com")

    def test_delete_client(self):
        deleted = self.service.delete_client(self.carlos.id)

        self.assertTrue(deleted)
        self.assertIsNone(self.service.get_client_by_id(self.carlos.id))

    def test_create_client_with_invalid_email_raises_error(self):
        with self.assertRaises(ValueError):
            self.service.create_client(10, "Ana Garcia", "email-invalido", "1122334455")


class ClientControllerTests(TestCase):

    def setUp(self):
        # Crear clientes de prueba en la base de datos
        self.juan = Client.objects.create(name="Juan Perez", email="juan.perez@gmail.com", phone="1122334455")
        self.maria = Client.objects.create(name="Maria Gomez", email="maria.gomez@gmail.com", phone="1166778899")
        self.carlos = Client.objects.create(name="Carlos Lopez", email="carlos.lopez@gmail.com", phone="1199887766")
        self.client = DjangoClient()

    def test_get_clients_via_api(self):
        response = self.client.get("/clients/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Juan Perez")

    def test_get_client_by_id_via_api(self):
        response = self.client.get(f"/clients/{self.maria.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Maria Gomez")

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
            f"/clients/{self.maria.id}/",
            data='{"name": "Maria Actualizada", "email": "maria.actualizada@mail.com", "phone": "1188997766"}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Maria Actualizada")

    def test_delete_client_via_api(self):
        response = self.client.delete(f"/clients/{self.carlos.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Cliente eliminado correctamente.")


class ProductControllerTests(TestCase):

    def setUp(self):
        # Crear productos de prueba en la base de datos
        self.mouse = Product.objects.create(name="Mouse Gamer", price=15000)
        self.keyboard = Product.objects.create(name="Teclado Mecanico", price=45000)
        self.smart_watch = Product.objects.create(name="Smart Watch", price=120000)
        self.client = DjangoClient()

    def test_get_products_via_api(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Mouse Gamer")

    def test_get_product_by_id_via_api(self):
        response = self.client.get(f"/products/{self.keyboard.id}/")

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
            f"/admin/products/{self.keyboard.id}/",
            data='{"name": "Teclado Profesional", "price": 55000}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Teclado Profesional")

    def test_admin_delete_product_via_api(self):
        response = self.client.delete(f"/admin/products/{self.smart_watch.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Producto eliminado correctamente.")


class SaleServiceTests(TestCase):

    def setUp(self):
        self.client_model = Client.objects.create(
            name="Juan Perez",
            email="juan.perez@gmail.com",
            phone="1122334455"
        )
        self.product = Product.objects.create(name="Mouse Gamer", price=15000)
        self.sale = Sale.objects.create(
            client=self.client_model,
            product=self.product,
            quantity=2,
            status="pending"
        )
        self.service = SaleService()

    def test_create_sale(self):
        sale = self.service.create_sale(
            self.client_model.id,
            self.product.id,
            3,
            "pending"
        )

        self.assertEqual(sale.client_id, self.client_model.id)
        self.assertEqual(sale.product_id, self.product.id)
        self.assertEqual(sale.quantity, 3)
        self.assertEqual(sale.total, 45000.0)

    def test_update_sale(self):
        sale = self.service.update_sale(self.sale.id, 4, "completed")

        self.assertEqual(sale.quantity, 4)
        self.assertEqual(sale.status, "completed")
        self.assertEqual(sale.total, 60000.0)

    def test_delete_sale(self):
        deleted = self.service.delete_sale(self.sale.id)

        self.assertTrue(deleted)
        self.assertIsNone(self.service.get_sale_by_id(self.sale.id))


class SaleControllerTests(TestCase):

    def setUp(self):
        self.client_model = Client.objects.create(
            name="Juan Perez",
            email="juan.perez@gmail.com",
            phone="1122334455"
        )
        self.product = Product.objects.create(name="Mouse Gamer", price=15000)
        self.sale = Sale.objects.create(
            client=self.client_model,
            product=self.product,
            quantity=2,
            status="pending"
        )
        self.client = DjangoClient()

    def test_get_sales_via_api(self):
        response = self.client.get("/sales/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["quantity"], 2)

    def test_create_sale_via_api(self):
        response = self.client.post(
            "/sales/",
            data=json.dumps({
                "client_id": self.client_model.id,
                "product_id": self.product.id,
                "quantity": 3,
                "status": "pending"
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["quantity"], 3)

    def test_update_sale_via_api(self):
        response = self.client.put(
            f"/sales/{self.sale.id}/",
            data=json.dumps({"quantity": 5, "status": "completed"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["quantity"], 5)
        self.assertEqual(response.json()["status"], "completed")

    def test_delete_sale_via_api(self):
        response = self.client.delete(f"/sales/{self.sale.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(f"/sales/{self.sale.id}/").status_code, 404)
