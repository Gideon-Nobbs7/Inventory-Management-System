from django.contrib import admin
from .models import InventoryEntry, InventoryTransaction
# Register your models here.


admin.site.register(InventoryEntry)
admin.site.register(InventoryTransaction)