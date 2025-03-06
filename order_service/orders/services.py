import requests
from rest_framework.exceptions import APIException, ValidationError

class ProductService:
    BASE_URL = "http://0.0.0.0:8001/products/api/v1/"

    def get_product(product_id):
        try:
            response = requests.get(f"{ProductService.BASE_URL}/{product_id}")
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            raise ValueError(f"Error fetching product: {str(e)}")


class InventoryService:
    def __init__(self):
        self.base_url = "http://0.0.0.0:8003/inventory/api/v1"

    def check_inventory(self, product_id:int, quantity:int):
        try:
            response = requests.get(f"{self.base_url}/{product_id}")
            if response.status_code == 404:
                raise ValidationError(f"Product {product_id} not found in inventory")
            
            inventory_data = response.json()
            if inventory_data["total_quantity"] < quantity:
                raise ValidationError(
                    f"Insufficient quantity available for product {product_id}"
                )
            
            return inventory_data
        
        except requests.RequestException as e:
            raise APIException("Inventory service temporarily unavailable")
        