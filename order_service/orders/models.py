from django.db import models
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    EVENT_TYPE_CHOICES = [
        ("ORDER_CREATED", "Order Created")
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled")
    ]
    user_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default="ORDER_CREATED")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")
    # shipping_address = models.CharField(max_length=200)
    # shipping_fee = models.PositiveIntegerField()
    # total_amount = models.IntegerField(null=False)

    # def save(self, *args, **kwargs):
    #     if isinstance(self.timestamp, str):
    #         self.timestamp = timezone.datetime.fromisoformat(self.timestamp)
    #         super().save(*args, **kwargs)

    def __str__(self):
        return self.pk

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product_id = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.IntegerField(null=False)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.order.pk
