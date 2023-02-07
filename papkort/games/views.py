# Create your views here.
from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Deck, Match, Player


def index(request):
    return redirect("matches")


def matches(request):
    matches = Match.objects.order_by('date')

    context = {'matches': matches}

    return render(request, 'matches/matches.html', context)


def decks(request):
    decks = Deck.objects.all()

    context = {'decks': decks}

    return render(request, 'matches/decks.html', context)


def stats(request):
    players = Player.objects.all()

    person_positions = defaultdict(list)
    deck_positions = defaultdict(list)

    for player in players:
        person_positions[player.person].append(player.position)
        deck_positions[player.deck].append(player.position)

    person_win_percentage = []
    for person, positions in person_positions.items():
        person_win_percentage.append({
            "person": person.__str__(),
            "percentage": positions.count(1) / len(positions) * 100
        })

    deck_win_percentage = []
    for deck, positions in deck_positions.items():
        print("NIGGERS", dir(deck.color))
        deck_win_percentage.append({
            "deck": deck.__str__(),
            "percentage": positions.count(1) / len(positions) * 100
        })

    context = {
        'person_win_percentage': sorted(person_win_percentage, key=lambda x: x["percentage"], reverse=True),
        'deck_win_percentage': sorted(deck_win_percentage, key=lambda x: x["percentage"], reverse=True)
    }

    return render(request, 'matches/stats.html', context)

