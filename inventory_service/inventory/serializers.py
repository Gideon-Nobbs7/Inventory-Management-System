from rest_framework import serializers
from .models import InventoryEntry


class InventoryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryEntry
        fields = ["product_id", "total_quantity", "reserved_quantity", "min_stock_level", "status", "unit_location"]