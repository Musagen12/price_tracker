from celery import Celery
from celery.schedules import crontab
from api.jumia.queries import automate_jumia
from api.amazon.queries import automate
from .config import redis_url
from sqlalchemy.orm import Session
from api.database import get_db
import asyncio

# Create a Celery instance
celery_app = Celery(__name__)

# Configure the broker and backend
celery_app.conf.broker_url = redis_url
celery_app.conf.result_backend = redis_url
celery_app.conf.broker_connection_retry_on_startup = True

# Import the scheduled tasks module to register tasks
from . import scheduled_tasks  # Ensure this import matches your module structure

@celery_app.task(name='scheduled_tasks.scrape_jumia_tracked_items')
def scrape_jumia_tracked_items():
    # Get a new database session
    generator = get_db()  # This is a generator
    db = next(generator)  # Retrieve the session from the generator

    try:
        asyncio.run(automate_jumia(db))  # Pass the session to the automate function
    finally:
        generator.close()

@celery_app.task(name='scheduled_tasks.scrape_tracked_items')
def scrape_tracked_items():
    # Get a new database session
    db_generator = get_db()  # This is a generator
    db = next(db_generator)  # Retrieve the session from the generator

    try:
        automate(db)  # Pass the session to the automate function
    finally:
        db_generator.close() 

# Define the beat schedule
celery_app.conf.beat_schedule = {
    'run-every-20-minutes': {
        'task': 'scheduled_tasks.scrape_tracked_items',
        'schedule': crontab(minute='*/20'),
    },
    'run-jumia': {
        'task': 'scheduled_tasks.scrape_jumia_tracked_items',
        'schedule': crontab(minute='*/20'),  # Adjust this as needed
    },
}

# Set the timezone
celery_app.conf.timezone = 'Africa/Nairobi'
