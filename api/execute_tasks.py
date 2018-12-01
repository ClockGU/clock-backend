from api.tasks import twenty_second_task

# Proof of concept, run this to see that celery is working

if __name__ == "__main__":
    for _ in range(10):
        twenty_second_task.delay()

