from django.http import HttpResponse
from api.tasks import twenty_second_task, async_5_user_creation
import random

# Proof of Concept that celery works

def index(request):
    async_5_user_creation.delay()
    return HttpResponse("A Dummy site.")
