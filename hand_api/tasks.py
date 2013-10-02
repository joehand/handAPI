from __future__ import absolute_import
from celery import Celery

from .twitter import Tweets
from .user import User

celery = Celery("tasks",
                broker='redis://localhost:6379/0',
                backend='redis')

@celery.task(name="tasks.add")
def add(x, y):
    return x + y


@celery.task(name="tasks.twitter")
def twitter(user):
    return 

if __name__ == "__main__":
    celery.start()