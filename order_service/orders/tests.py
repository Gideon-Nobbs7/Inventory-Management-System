from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from unittest.mock import patch, Mock
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import Order, OrderItem
from .authentication import MicroserviceAuthentication, MicroserviceUser
# from .producer import publish_order
import jwt, pika, json
from datetime import datetime, timedelta
# Create your tests here.   


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testUser",
            password="testorder25"
        )
        self.client = APIClient()

        self.user_data = {
            "sub": "1",
            "id": 1,
            "user_id": "12",
            "username": "testUser",
            "email": "testemail@gmail.com"
        }

        self.jwt_secret = "giiiid"

        current_time = datetime.now()
        exp = current_time + timedelta(hours=1)

        self.token_payload = {
            **self.user_data,
            "exp": int(exp.timestamp()),
            "iat": int(current_time.timestamp()),
        }

        token = AccessToken()

        token["user_id"] = "12"
        token["username"] = "testUser"
        token["email"] = "tokenEmail@gmail.com"

        self.token = str(token)

        self.order_data = {
            "user_id": 12,
            "event_type": "ORDER_CREATED",
            "status": "PENDING",
            "order_items": [
                {
                    "product_id": "1",
                    "quantity": 20,
                    "unit_price": 2.00,
                    "total": 40
                }
            ]
        }

        self.order_url = reverse("order-viewset")
    

    @patch('orders.authentication.MicroserviceAuthentication')
    @patch('pika.BlockingConnection')
    def test_create_order_valid_token(self, mock_user_service, mock_connection):
        mock_user_service.return_value = MicroserviceUser(user_id="12")

        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        response = self.client.post(self.order_url, self.order_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        mock_channel.queue_declare.assert_called_with(queue="main_orders")

        publish_calls = mock_channel.basic_publish.call_args_list
        if publish_calls:
            args=publish_calls[0][1]
            published_message = json.loads(args['body'])
            print(f"Published message : {published_message}")

            self.assertIn("event_type", published_message)
            self.assertIn("order_id", published_message)
            self.assertIn("items", published_message)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    @patch('orders.authentication.MicroserviceAuthentication')
    @patch('pika.BlockingConnection')
    def test_create_order_inventory_error(self, mock_user_service, mock_connection):
        # test_user = MicroserviceUser(user_id="12")
        mock_user_service.return_value = MicroserviceUser(user_id="12")

        mock_connection.side_effect = pika.exceptions.AMQPConnectionError("Connection failed")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        
        response = self.client.post(self.order_url, self.order_data, format='json')
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content}")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"detail": "Inventory service temporarily unavailable"})
