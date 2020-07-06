from .tasks import twenty_second_task

# Proof of concept, run this to see that celery is working

if __name__ == "__main__":
    twenty_second_task.delay(1)
    twenty_second_task.delay(1)
