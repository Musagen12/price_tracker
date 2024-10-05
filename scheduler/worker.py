import pika
import json
from sqlalchemy.orm import Session
from api.jumia.queries import automate_jumia
from api.database import get_db

def process_task(ch, method, properties, body):
    task = json.loads(body)
    print(f" [x] Received {task}")

    if task['task_name'] == 'automate':
        # Get a new database session
        generator = get_db()  # This is a generator
        db = next(generator)  # Retrieve the session from the generator

        try:
            automate_jumia(db)  # Call your automate function with the DB session
        finally:
            generator.close()  # Close the session

    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message

def start_worker(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_qos(prefetch_count=1)  # Only fetch one message at a time
    channel.basic_consume(queue=queue_name, on_message_callback=process_task)

    print(f" [*] Waiting for tasks on '{queue_name}'. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker('automate_tasks')
