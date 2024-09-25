# from celery import Celery
# from celery.schedules import crontab
# from .config import redis_url
# from . import scheduled_tasks

# celery_app = Celery(__name__)

# celery_app.conf.broker_url = redis_url
# celery_app.conf.result_backend = redis_url
# celery_app.conf.broker_connection_retry_on_startup = True

# celery_app.conf.beat_schedule = {
#     'run-every-30-minutes': {
#         'task': 'scheduled_tasks.scrape_tracked_items',
#         'schedule': crontab(minute='*/3'),  
#     },
# }

# celery_app.conf.timezone = 'Africa/Nairobi'  

# from celery import Celery
# from celery.schedules import crontab
# from api.amazon.queries import automate
# from .config import redis_url

# celery_app = Celery(__name__)

# celery_app.conf.broker_url = redis_url
# celery_app.conf.result_backend = redis_url
# celery_app.conf.broker_connection_retry_on_startup = True

# @celery_app.task
# def scrape_tracked_items():
#     automate()

# celery_app.conf.beat_schedule = {
#     'run-every-3-minutes': {
#         'task': 'scheduled_tasks.scrape_tracked_items',
#         'schedule': crontab(minute='*/3'),
#     },
# }

# celery_app.conf.timezone = 'Africa/Nairobi'

# from . import scheduled_tasks  


from celery import Celery
from celery.schedules import crontab
from api.amazon.queries import automate
from .config import redis_url
from sqlalchemy.orm import Session
from api.database import get_db 

celery_app = Celery(__name__)

celery_app.conf.broker_url = redis_url
celery_app.conf.result_backend = redis_url
celery_app.conf.broker_connection_retry_on_startup = True

@celery_app.task(name='scheduled_tasks.scrape_tracked_items')
def scrape_tracked_items():
    # Get a new database session
    db_generator = get_db()  # This is a generator
    db = next(db_generator)  # Retrieve the session from the generator

    try:
        automate(db)  # Pass the session to the automate function
    finally:
        db_generator.close() 


celery_app.conf.beat_schedule = {
    'run-every-20-minutes': {
        'task': 'scheduled_tasks.scrape_tracked_items',
        'schedule': crontab(minute='*/20'),
    },
}

celery_app.conf.timezone = 'Africa/Nairobi'

