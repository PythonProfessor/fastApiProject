import asyncio
import time
from time import sleep
from celery import Celery
from celery.utils.log import get_task_logger
from Valhalla.valhalla import Vallhala

# Initialize celery

celery = Celery('tasks', broker='amqp://guest:guest@127.0.0.1:5672//')
# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)


# Create Order - Run Asynchronously with celery
# Example process of long running task

@celery.task
def heal_rabbits():
    # Display log
    print("Zashli v funciyu")
    asyncio.sleep(2)
    x = Vallhala()
    x.start()
    celery_log.info(f"Rabbits have been healed")
