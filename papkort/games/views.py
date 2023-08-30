from collections import defaultdict

from django.db.models import Case, Count, IntegerField, When
from django.shortcuts import redirect, render
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.db.models import Q, F
from .models import Deck, Match, Person, Player
from openskill.models import PlackettLuce

COLOR_ORDER = {
    'w': 0, 'u': 1, 'b': 2, 'r': 3, 'g': 4, 'colorless': 5,
    'wu': 6, 'ub': 7, 'br': 8, 'rg': 9, 'gw': 10,
    'wb': 11, 'ur': 12, 'bg': 13, 'rw': 14, 'gu': 15,
    'wub': 16, 'ubr': 17, 'brg': 18, 'rgw': 19, 'gwu': 20,
    'wbg': 21, 'urw': 22, 'bgu': 23, 'rwb': 24, 'gur': 25,
    'wubr': 26, 'ubrg': 27, 'brgw': 28, 'rgwu': 29, 'gwub': 30,
    'wubrg': 31
}


def index(request):
    return redirect("matches")


def matches(request):
    all_matches = Match.objects.order_by('-date').prefetch_related('players', 'players__deck', 'players__person')

    context = {'matches': all_matches}

    return render(request, 'matches/matches.html', context)


def person_stats(request, person_id):
    # Count the number of matches played by the person
    matches = Match.objects.prefetch_related('players', 'players__deck', 'players__person').annotate(player_count=Count('players')).filter(players__person_id=person_id)
    matches_4p = matches.filter(player_count=4)
    matches_3p = matches.filter(player_count=3)
    num_matches = matches.count()
    num_matches_4p = matches_4p.count()
    num_matches_3p = matches_3p.count()

    # Count the number of wins by the person
    all_wins = Player.objects.prefetch_related('person', 'deck', 'match').filter(position=1, person_id=person_id)
    num_wins = all_wins.count()
    num_wins_4p = all_wins.filter(match__in=matches_4p).count()
    num_wins_3p = all_wins.filter(match__in=matches_3p).count()

    # Compute the win percentage of the person
    win_percentage = f'{int(num_wins / num_matches * 100)}%' if num_matches > 0 else 'N/A'
    win_percentage_4p = f'{int(num_wins_4p / num_matches_4p * 100)}%' if num_matches_4p > 0 else 'N/A'
    win_percentage_3p = f'{int(num_wins_3p / num_matches_3p * 100)}%' if num_matches_3p > 0 else 'N/A'

    person = Person.objects.get(id=person_id)

    color_counts = defaultdict(lambda: defaultdict(int))

    # Count the number of times each color was played by the person
    color_identity_counts = person.player_set.values('deck__color').annotate(count=Count('deck__color'))
    # Append pretty color choice name
    for color_identity_count in color_identity_counts:
        color_identity_count['color_name'] = dict(Deck.Color.choices)[color_identity_count['deck__color']]

        for color in color_identity_count['deck__color']:
            color_counts[color]['count'] += color_identity_count['count']
            color_counts[color]['color_name'] = dict(Deck.Color.choices)[color] # yeah, I know
            color_counts[color]['color'] = color  # yeah, I know

    # We do this to count the plays and wins for the specific player and the deck
    deck_counts = Deck.objects.filter(player__person=person).annotate(
        count=Count('player__deck'),
        wins=Count(Case(When(player__position=1, then=1), output_field=IntegerField()))
    ).order_by('-count')

    for d in deck_counts:
        d.win_percentage = f'{int(d.wins / d.count * 100)}%'

    # This win percentage on decks is shown no matter who played it
    owned_decks = Deck.objects.filter(owner=person).prefetch_related('player_set', 'player_set__person', 'owner').annotate(
        win_count=Count('player', filter=Q(player__position=1)),
        played_count=Count('player'),
        win_percentage=Cast(Cast(F('win_count'), FloatField()) / F('played_count') * 100.0, IntegerField())
    )

    if request.GET.get('ordering') == 'win':
        owned_decks = sorted(owned_decks, key=lambda x: x.win_count / x.played_count, reverse=True)
    elif request.GET.get('ordering') == 'total':
        owned_decks = sorted(owned_decks, key=lambda x: x.played_count, reverse=True)
    else:
        owned_decks = sorted(owned_decks, key=lambda x: COLOR_ORDER[x.color])

    context = {
        'person': person,
        'num_matches': num_matches,
        'num_wins': num_wins,
        'win_percentage': win_percentage,
        'num_matches_3p': num_matches_3p,
        'num_wins_3p': num_wins_3p,
        'win_percentage_3p': win_percentage_3p,
        'num_matches_4p': num_matches_4p,
        'num_wins_4p': num_wins_4p,
        'win_percentage_4p': win_percentage_4p,
        'deck_colors': color_identity_counts,
        'deck_counts': deck_counts,
        'color_counts': sorted(color_counts.values(), key=lambda x: x['count'], reverse=True),
        'decks': owned_decks
    }

    return render(request, 'matches/person.html', context)


def players(request):
    all_players = Player.objects.prefetch_related('match', 'deck', 'person', 'person__deck_set').annotate(match_player_count=Count('match__players'))

    player_data = defaultdict(lambda: {
        'person': None,
        'games_played': 0,
        'games_won': 0,
        '4p_games_played': 0,
        '4p_games_won': 0,
        '3p_games_played': 0,
        '3p_games_won': 0,
        'colors': {
            'w': 0,
            'u': 0,
            'r': 0,
            'b': 0,
            'g': 0,
            'colorless': 0
        },
        'deck_plays': defaultdict(int)
    })

    # Yeah, I know this gets slow at some point
    for player in all_players:
        player_data[player.person]['person'] = player.person
        player_data[player.person]['games_played'] += 1
        player_data[player.person]['games_won'] += 1 if player.position == 1 else 0
        if player.match_player_count == 4:
            player_data[player.person]['4p_games_played'] += 1
            player_data[player.person]['4p_games_won'] += 1 if player.position == 1 else 0
        if player.match_player_count == 3:
            player_data[player.person]['3p_games_played'] += 1
            player_data[player.person]['3p_games_won'] += 1 if player.position == 1 else 0
        player_data[player.person]['deck_plays'][player.deck] += 1

        if player.deck.color == 'colorless':
            player_data[player.person]['colors'][player.deck.color] += 1
        else:
            for color in player.deck.color:
                player_data[player.person]['colors'][color] += 1

    # Calc win percentage most played color stuff lolo
    for entry in player_data.values():
        entry['win_percentage'] = int(entry['games_won'] / entry['games_played'] * 100)
        entry['4p_win_percentage'] = int(entry['4p_games_won'] / entry['4p_games_played'] * 100) if entry['4p_games_played'] else 'N/A'
        entry['3p_win_percentage'] = int(entry['3p_games_won'] / entry['3p_games_played'] * 100) if entry['3p_games_played'] else 'N/A'
        entry['favorite_color'] = max(entry['colors'], key=entry['colors'].get)
        entry['owned_decks'] = entry['person'].deck_set.count
        entry['favorite_deck'] = max(entry['deck_plays'], key=entry['deck_plays'].get)
        entry['favorite_deck_plays'] = entry['deck_plays'][entry['favorite_deck']]

    context = {'players': sorted(player_data.values(), key=lambda x: x['win_percentage'], reverse=True)}

    return render(request, 'matches/players.html', context)


def decks(request):
    all_decks = Deck.objects.all().prefetch_related('player_set', 'player_set__person', 'owner').annotate(
        win_count=Count('player', filter=Q(player__position=1)),
        played_count=Count('player'),
        win_percentage=Cast(Cast(F('win_count'), FloatField()) / F('played_count') * 100.0, IntegerField())
    )

    if request.GET.get('ordering') == 'win':
        context = {'decks': sorted(all_decks, key=lambda x: x.win_count / x.played_count, reverse=True)}
    elif request.GET.get('ordering') == 'total':
        context = {'decks': sorted(all_decks, key=lambda x: x.played_count, reverse=True)}
    else:
        context = {'decks': sorted(all_decks, key=lambda x: COLOR_ORDER[x.color])}
    return render(request, 'matches/decks.html', context)


def stats(request):
    all_players = Player.objects.prefetch_related('match', 'deck', 'person')

    person_positions = defaultdict(list)
    deck_positions = defaultdict(list)
    color_positions = defaultdict(list)
    person_deck_color = defaultdict(lambda: defaultdict(int))
    color_wins = defaultdict(int)

    for player in all_players:
        person_positions[player.person].append(player.position)
        deck_positions[player.deck].append(player.position)
        color_positions[player.deck.get_color_display()].append(player.position)

        if player.position == 1:
            for c in player.deck.extract_colors():
                color_wins[c] += 1

        if player.deck.color == 'colorless':
            person_deck_color[player.person.name][player.deck.color] += 1
        else:
            for color in player.deck.color:
                person_deck_color[player.person.name][color] += 1

    #AAH DET ER FLAWED FORDI DEN TÆLLER PLAYS OG IKKE DECKS
    person_deck_colors = []
    for person, colors in person_deck_color.items():
        colors['name'] = person
        person_deck_colors.append(dict(colors))

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

    color_win_percentage = []
    for color, positions in color_positions.items():
        color_win_percentage.append({
            "color": color,
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
        'color_win_percentage': sorted(color_win_percentage, key=lambda x: x["percentage"], reverse=True),
        'deck_colors': deck_colors,
        'color_wins': dict(color_wins),
        'person_deck_colors': person_deck_colors
    }

    return render(request, 'matches/stats.html', context)


def ranks(request):
    matches = Match.objects.order_by('id').prefetch_related('players', 'players__person', 'players__deck')
    persons = Person.objects.all()
    model = PlackettLuce()

    player_ranks = {p.name: model.rating(name=p.name) for p in persons}

    for m in matches:
        match = []
        match_ranks = []

        for p in m.players.all():
            match.append([player_ranks[p.person.name]])
            if p.position == 1:
                match_ranks.append(1)
            else:
                match_ranks.append(2)

        new_ranks = model.rate(match, ranks=match_ranks)

        for rank in [rank for teams in new_ranks for rank in teams]:
            # Replace with updated rank
            player_ranks[rank.name] = rank

    context = {
        'ranks': sorted(player_ranks.items(), key=lambda x: x[1].ordinal(), reverse=True)
    }

    return render(request, 'matches/ranks.html', context)


