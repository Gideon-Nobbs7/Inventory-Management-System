from django.db import transaction
import json, pika, os
from dotenv import load_dotenv
from .models import InventoryEntry, InventoryTransaction, ProcessMessage

load_dotenv() 

class InventoryConsumer:
    def __init__(self):
        self.url = os.getenv("AMQP_KEY")
        self.params = pika.URLParameters(self.url)
        self.params.socket_timeout = 2
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="new_orders")
    
    def consume(self):
        self.channel.basic_consume(
            queue="order_events",
            on_message_callback=self.process_order_message,
            auto_ack=False
        )
        self.channel.start_consuming()

    def process_order_message(self, channel, method, property, body):
        try:
            message = json.loads(body)
            print(message)

            order_id = message.get("order_id")

            with transaction.atomic():
                processed, created = ProcessMessage.objects.get_or_create(
                    message_id=order_id
                )

                if created and message["event_type"] == "ORDER_CREATED":

                    items = json.loads(message["items"])

                    for item in items:
                        try:
                            inventory_entry = InventoryEntry.objects.get(product_id=item["product_id"])
                            if inventory_entry.total_quantity == 0:
                                raise ValueError("The quantity for this product is finished")
                            inventory_entry.total_quantity -= item["quantity"]
                            inventory_entry.save()
                        
                            InventoryTransaction.objects.create(
                                inventory_entry=inventory_entry,
                                product_id=item["product_id"],
                                quantity_change=item["quantity"],
                                transaction_type="SALE"
                            )
                        except InventoryEntry.DoesNotExist:
                            print(f"Inventory not found for product {item["product_id"]}")
                            raise
            channel.basic_ack(delivery_tag=method.delivery_tag)
        
        except Exception as e:
        # Explicitly handle potential channel issues
            print(f"Error hanndling consume {str(e)}")
        try:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as nack_error:
            print(f"Error sending nack: {str(nack_error)}")
                    



    