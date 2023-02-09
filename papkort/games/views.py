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

    order = {
        'w': 0, 'u': 1, 'b': 2, 'r': 3, 'g': 4, 'colorless': 5,
        'wu': 6, 'ub': 7, 'br': 8, 'rg': 9, 'gw': 10,
        'wb': 11, 'ur': 12, 'bg': 13, 'rw': 14, 'gu': 15,
        'wub': 16, 'ubr': 17, 'brg': 18, 'rgw': 19, 'gwu': 20,
        'wbg': 21, 'urw': 22, 'bgu': 23,  'rwb': 24,  'gur': 25,
        'wubr': 26, 'ubrg': 27, 'brgw': 28, 'rgwu': 29, 'gwub': 30,
        'wubrg': 31
    }

    context = {'decks': sorted(decks, key=lambda x: order[x.color])}

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
        deck_win_percentage.append({
            "deck": deck.__str__(),
            "percentage": positions.count(1) / len(positions) * 100
        })

    deck_colors = {
        'w' : 0,
        'u': 0,
        'r': 0,
        'b': 0,
        'g': 0,
        'colorless': 0
    }

    for d in Deck.objects.all():
        if d.color == 'colorless':
            deck_colors[d.color] += 1
        else:
            for color in d.color:
                deck_colors[color] += 1

    context = {
        'person_win_percentage': sorted(person_win_percentage, key=lambda x: x["percentage"], reverse=True),
        'deck_win_percentage': sorted(deck_win_percentage, key=lambda x: x["percentage"], reverse=True),
        'deck_colors': deck_colors,
    }

    return render(request, 'matches/stats.html', context)

