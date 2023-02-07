# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from .models import Deck, Match


def index(request):
    return HttpResponse("Hello, this is games app")


def matches(request):
    matches = Match.objects.order_by('date')

    context = {'matches': matches}

    return render(request, 'matches/matches.html', context)


def decks(request):
    decks = Deck.objects.all()

    context = {'decks': decks}

    return render(request, 'matches/decks.html', context)

