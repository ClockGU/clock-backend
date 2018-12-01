from __future__ import absolute_import
from celery import Celery
app = Celery('clock-backend',
             broker='amqp://broker_adm:broker_pass@rabbit_broker:5672',
             backend='rpc://',
             include=['api.tasks'])
