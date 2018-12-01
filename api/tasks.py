from __future__ import absolute_import
import time
from .celery import app

# 20 Second running Tasks


@app.task(bind=True, default_retry_delay=10)
def twenty_second_task(self):
    print("This Task starts.")
    time.sleep(20)
    print("This Task ends.")


@app.task(bind=True, default_retry_delay=10)
def forty_print_task(self):
    for i in range(40):
        print("Current count is {}.".format(i))
        time.sleep(2)

