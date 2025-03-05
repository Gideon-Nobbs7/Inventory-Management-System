from django.db import models

# Create your models here.

class NotificationModel(models.Model):
    types = (
        ("LOW_STOCK", "Low Stock"),
        ("ORDER_STATUS", "Order Status"),
        ("DELIVERY_UPDATE", "Delivery Update")
    )

    status_levels = (
        ("PENDING", "Pending"),
        ("SENT", "Sent"),
        ("FAILED", "Failed")
    )

    priority_levels = (
        ("SERIOUS", "Serious"),
        ("MILD", "Mild"),
        ("NORMAL", "Normal")
    )

    type_of_channel = (
        ("EMAIL", "Email"),
        ("SMS", "Sms"),
    )

    type = models.CharField(max_length=20, choices=types, default="ORDER_STATUS")
    recipient_name = models.CharField(max_length=150)
    recipient_email = models.EmailField()
    content = models.CharField(max_length=200)
    priority_level = models.CharField(max_length=15, choices=priority_levels, default="NORMAL")
    status = models.CharField(max_length=15, choices=status_levels, default="SENT")
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=15, choices=type_of_channel, default="EMAIL")

    def __str__(self):
        return f"{self.name} - {self.type}"

