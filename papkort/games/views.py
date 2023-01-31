# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, this is games app")


def games(request):
    print("hej")
    return HttpResponse("Hello, this is games")


def decks(request):
    return HttpResponse("Hello, this is decks")
