from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings


# Create your views here.
def index(request: HttpRequest):
    title = settings.TITLE
    return render(request, "index.html", locals())
