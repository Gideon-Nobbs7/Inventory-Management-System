from rest_framework import serializers
from .models import Order, OrderItem
from .services import ProductService, InventoryService
from .producer import publish_order

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product_id", "quantity", "unit_price"]


        def create(self, validated_data):
            product_id = validated_data.get("product_id")
            quantity = validated_data.get("quantity")

            product_service = ProductService()
            inventory_service = InventoryService()

            product_data = product_service.get_product(product_id)
            if not product_data:
                raise serializers.ValidationError(f"Product with ID {product_id} not found")
            
            inventory_service.check_inventory(product_id, quantity)
            
            unit_price = product_data["price"]
            total = unit_price * quantity

            validated_data["unit_price"] = unit_price
            validated_data["total"] = total

            return OrderItem.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ["pk", "event_type", "order_items", "user_id", "status"]
        read_only_fields = ['user_id']
    

    def create(self, validated_data):
        user_id = self.context["request"].user.id
        validated_data["user_id"] = user_id

        order_items_data = validated_data.pop("order_items")

        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            item_data["order"] = order
            OrderItemSerializer().create(item_data)

        publish_order(order, order_items_data)

        return order 

