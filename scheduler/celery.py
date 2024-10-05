from celery import Celery
from celery.schedules import crontab
from api.amazon.queries import automate
from .config import redis_url
from sqlalchemy.orm import Session
from api.database import get_db
import asyncio

celery_app = Celery(__name__)

celery_app.conf.broker_url = redis_url
celery_app.conf.result_backend = redis_url
celery_app.conf.broker_connection_retry_on_startup = True

@celery_app.task(name='scheduled_tasks.scrape_tracked_items')
def scrape_tracked_items():
    db_generator = get_db()  
    db = next(db_generator) 

    try:
        automate(db)  
    finally:
        db_generator.close() 

celery_app.conf.beat_schedule = {
    'run-every-20-minutes': {
        'task': 'scheduled_tasks.scrape_tracked_items',
        'schedule': crontab(minute='*/20'),
    },
}

celery_app.conf.timezone = 'Africa/Nairobi'
