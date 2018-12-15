from django.http import HttpResponse
from api.tasks import twenty_second_task, twenty_second_user
import random


def index(request):
    i = random.randint(0, 1000)
    twenty_second_user.delay(i)
    return HttpResponse("A Dummy site.")
