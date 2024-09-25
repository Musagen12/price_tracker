import os
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL")
print(redis_url)