from rest_framework import serializers
from .models import InventoryEntry


class InventoryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryEntry
        fields = ["product_id", "total_quantity", ""]