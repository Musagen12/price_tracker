import pika
import json
from apscheduler.schedulers.background import BackgroundScheduler
import time

def publish_task(queue_name, task_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(task_data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the task persistent
        )
    )
    print(f" [x] Sent {task_data}")
    connection.close()

def schedule_automate():
    # Task data for Amazon automation
    task_data_amazon = {
        "task_name": "automate"
    }
    publish_task('automate_tasks', task_data_amazon)

    # Task data for Jumia automation
    task_data_jumia = {
        "task_name": "automate_jumia"
    }
    publish_task('automate_tasks', task_data_jumia)

# Set up the scheduler
scheduler = BackgroundScheduler()
# Schedule the function to run every 20 minutes
scheduler.add_job(schedule_automate, 'interval', minutes=6)
scheduler.start()

try:
    # Keep the script running
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
