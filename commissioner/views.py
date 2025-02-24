from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


# Create your views here.
def index(request):
    return HttpResponse("Hello World. You're at the commissioners index page.")


@require_http_methods(["GET", "POST"])
def bet(request):
    pass
