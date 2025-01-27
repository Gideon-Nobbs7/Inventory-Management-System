from django.core.management.base import BaseCommand
from inventory.consumer import InventoryConsumer


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        consumer = InventoryConsumer()
        consumer.consume()