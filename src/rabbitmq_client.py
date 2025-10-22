import pika
import os
import json
import logging

logging.basicConfig(level=logging.INFO)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")
QUEUE_NAME = 'canvas_creation_queue'

def publish_message(message_body: dict):
    """
    Publica un mensaje en la cola de creación de canvas.
    """
    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()

        # Declara la cola (es idempotente, solo la crea si no existe)
        # durable=True asegura que la cola sobreviva a reinicios de RabbitMQ
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=json.dumps(message_body),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Hace el mensaje persistente
            ))
        logging.info(f" [x] Sent {message_body} to queue '{QUEUE_NAME}'")
        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Error connecting to RabbitMQ: {e}")
        # En un caso real, podrías reintentar o usar un fallback.
        # Por ahora, lanzamos la excepción para que el endpoint falle.
        raise ConnectionError("Could not connect to RabbitMQ service") from e
