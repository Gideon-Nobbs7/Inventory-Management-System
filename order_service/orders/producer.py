import pika, os, json
from dotenv import load_dotenv
from . import serializers

load_dotenv()


def publish_order(order, order_items):
        url = os.getenv("AMQP_KEY")
        params = pika.URLParameters(url)
        params.socket_timeout = 2

        try:
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue="main_order", durable=True)

            serialized_items = serializers.OrderItemSerializer(order_items, many=True).data

            message = {
                "event_type": "ORDER_CREATED",
                "order_id": str(order.id),
                "items": json.dumps(serialized_items)
            }

            channel.basic_publish(
                exchange='',
                routing_key="main_order",
                body = json.dumps(message)
            )
            print("Order successfully published")
            print(message)
            connection.close()

        except Exception as e:
            print(f"Error Publishing Message: {str(e)}")