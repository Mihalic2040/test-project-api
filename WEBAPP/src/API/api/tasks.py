from celery import shared_task
import os
from celery import Celery 


celery = Celery('tasks', broker='redis://redis:6379')

os.environ["DJANGO_SETTINGS_MODULE"] = "main.settings"

@shared_task()
def log_console():
    print("Im log")
    return True