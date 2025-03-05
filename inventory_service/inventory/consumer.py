from django.db import transaction
import json, pika, os
from dotenv import load_dotenv
from environs import Env
from .producer import publish_to_notif
from .models import InventoryEntry, InventoryTransaction, ProcessMessage

load_dotenv() 

env = Env()
env.read_env()

class InventoryConsumer:
    def __init__(self):
        self.url = os.environ.get("AMQP_KEY")
        self.params = pika.URLParameters(self.url)
        self.params.socket_timeout = 5
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="main_order", durable=True)
    
    def consume(self):
        self.channel.basic_consume(
            queue="main_order",
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

                if not created:
                    channel.basic_ack(delivery_tag=method.delivery_tag)

                if message["event_type"] == "ORDER_CREATED":

                    items = json.loads(message["items"])

                    for item in items:
                        try:
                            inventory_entry = InventoryEntry.objects.get(product_id=item["product_id"])
                            if inventory_entry.total_quantity == 0:
                                raise ValueError("The quantity for this product is finished")
                            
                            elif inventory_entry.is_low_stock:
                                publish_to_notif(inventory_entry)

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
            if not channel.is_closed:
                channel.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as nack_error:
            print(f"Error sending nack: {str(nack_error)}")
                    



    