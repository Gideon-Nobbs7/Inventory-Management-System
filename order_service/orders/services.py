import requests


class ProductService:
    BASE_URL = "localhost:8002/products/api/v1/"

    def get_product(product_id):
        try:
            response = requests.get(f"{ProductService.BASE_URL}/{product_id}")
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            raise ValueError(f"Error fetching product: {str(e)}")
        