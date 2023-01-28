from asyncio import tasks
from django.http import HttpResponse
from . import tasks
# Create your views here.

def home(request):

    tasks.log_console.delay()

    return HttpResponse("Hello World")
