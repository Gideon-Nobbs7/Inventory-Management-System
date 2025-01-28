from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


class ProductTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testUser",
            password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100,
            quantity=1200
        )
        self.product_url = reverse("product-detail", args=[self.product.id])
        self.products_url = reverse("product-create")

    def test_product_list(self):
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Test Product")

    def test_get_product_detail(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Product")
        self.assertEqual(response.data["price"], 100)

    def test_create_product(self):
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': 187,
            'quantity': 1500
        }
        response = self.client.post(self.products_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Product")

    def test_update_product(self):
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': 290,
            'quantity': 300
        }
        response = self.client.put(self.product_url, data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["description"], "Updated Description")

    def test_delete_product(self):
        response = self.client.delete(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)



class TestProductSerializer(APITestCase):
    def test_product_serializer_valid_data(self):
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': 187,
            'quantity': 1500
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.name, "New Product")

    def test_product_serializer_invalid_data(self):
        data = {
            'name': '',
            'description': 'New Description',
            'price': -198,
            'quantity': 1500
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('price', serializer.errors)
