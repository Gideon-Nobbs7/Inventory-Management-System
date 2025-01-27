from django.db import models

# Create your models here.

class InventoryEntry(models.Model):
    STATUS_CHOICES = [
        ("IN_STOCK", "In Stock"),
        ("LOW_STOCK", "Low Stock"),
        ("OUT_OF_STOCK", "Out of Stock")
    ]

    UNIT_LOCATION = [
        ("AISLE", "Aisle"),
        ("RACK", "Rack"),
        ("SHELF", "Shelf")
    ]

    product_id = models.CharField(max_length=10)
    total_quantity = models.PositiveIntegerField()
    reserved_quantity = models.PositiveIntegerField()
    min_stock_level = models.PositiveIntegerField(default=10)
    max_stock_level = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="IN_STOCK")
    unit_location = models.CharField(max_length=20, choices=UNIT_LOCATION, default="SHELF")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def available_quantity(self):
        return self.total_quantity - self.reserved_quantity
    
    def is_low_stock(self):
        return self.available_quantity <= self.min_stock_level
    


class InventoryTransaction(models.Model):
    TRANSACTION_CHOICES = [
            ('RESTOCK', 'Restock'),
            ('SALE', 'Sale'),
            ('ADJUSTMENT', 'Manual Adjustment'),
            ('DAMAGED', 'Damaged Goods')
        ]
    
    inventory_entry = models.ForeignKey(InventoryEntry, on_delete=models.SET_NULL, null=True)
    product_id = models.CharField(max_length=10)
    quantity_change = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES, default="SALE")
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return f"{self.product_id} - {self.transaction_type}"
    

class ProcessMessage(models.Model):
    message_id = models.CharField(max_length=10)
    processed_at = models.DateTimeField(auto_now_add=True)
