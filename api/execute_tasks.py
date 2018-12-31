from api.tasks import twenty_second_task, twenty_second_user
import os
# Proof of concept, run this to see that celery is working

if __name__ == "__main__":
    twenty_second_task.delay(1)
    twenty_second_user.delay(1)
    # for i in range(10):
    #     twenty_second_task.delay(i)
    #     twenty_second_user.delay(i)

