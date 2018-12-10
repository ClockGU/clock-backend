from __future__ import absolute_import
from celery import Celery
import os


app = Celery('clock-backend',
             broker=os.environ.get('RABBITMQ_URL'),
             backend='rpc://',
             include=['api.tasks'])
