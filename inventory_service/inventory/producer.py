import pika, os, json
from dotenv import load_dotenv
from .serializers import InventoryEntrySerializer
load_dotenv()


def publish_to_notif(items):
    url = os.getenv("AMQP_KEY")
    params = pika.URLParameters(url)
    params.socket_timeout = 2

    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue="notif")

        serialized_items = InventoryEntrySerializer(items).data
        
        message = {
            "notif_type": "LOW_STOCK",
            "items": json.dumps(serialized_items)
        }
        print(message)

        channel.basic_publish(
            exchange="",
            routing_key="low_stock_events",
            body=json.dumps(message)
        )
        connection.close()

    except Exception as e:
        print(f"Error sending notification: {str(e)}")