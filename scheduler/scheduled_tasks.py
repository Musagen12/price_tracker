from celery import shared_task
from sqlalchemy.orm import Session
from api.jumia.queries import automate_jumia
from api.database import get_db

@shared_task(name='scheduled_tasks.scrape_jumia_tracked_items')
def scrape_jumia_tracked_items():
    # Get a new database session
    generator = get_db()  # This is a generator
    db = next(generator)  # Retrieve the session from the generator

    try:
        automate_jumia(db)  # Pass the session to the automate function
    finally:
        generator.close()
