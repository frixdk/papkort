import itertools
from collections import defaultdict

from openskill.models import PlackettLuce

from ..models import Match, Deck


class GameService:
    @staticmethod
    def calculate_deck_rankings():
        # Calculate deck rankings
        matches = Match.objects.order_by('id').prefetch_related('players', 'players__person', 'players__deck')
        decks = Deck.objects.all().prefetch_related('owner')
        model = PlackettLuce()

        deck_ranks = {d: model.rating(name=d) for d in decks}

        for m in matches:
            match = []
            match_ranks = []

            for p in m.players.all():
                match.append([deck_ranks[p.deck]])
                if p.position == 1:
                    match_ranks.append(1)
                else:
                    match_ranks.append(2)

            new_ranks = model.rate(match, ranks=match_ranks)

            for rank in [rank for teams in new_ranks for rank in teams]:
                # Replace with updated rank
                deck_ranks[rank.name] = rank

        return deck_ranks

    @staticmethod
    def matchmaking(persons):
        deck_ranks = GameService.calculate_deck_rankings()

        person_ranks = defaultdict(list)

        for deck, rank in deck_ranks.items():
            if deck.name and "pauper" in deck.name.lower():
                continue

            person_ranks[deck.owner].append(rank)

        model = PlackettLuce()

        possible_decks = []
        for person in persons:
            possible_decks.append(person_ranks[person])

        bab = itertools.product(*possible_decks)

        matches = []

        for pos in bab:
            teams = []
            #print("¤"*40)
            for p in pos:
                #print(p.name)
                teams.append([p])
            bab = model.predict_win(teams)
            hej = sum([abs(0.25 - b) for b in bab])
            #print(bab)
            #print(hej)

            matches.append((pos, hej, bab))

        matches.sort(key=lambda x: x[1])

        return matches

        #p = itertools.product([1, 2], [3],[4],[5,6])

        # print(person_ranks)

    @staticmethod
    def matchmaking2(persons_with_decks):
        deck_ranks = GameService.calculate_deck_rankings()

        person_ranks = defaultdict(list)

        for deck, rank in deck_ranks.items():
            # Det er noget hax det her. Vi laver det bedre til sommer
            if deck.owner not in persons_with_decks.keys():
                continue

            if deck.name and "pauper" in deck.name.lower():
                continue

            if persons_with_decks[deck.owner] and deck not in persons_with_decks[deck.owner]:
                continue

            person_ranks[deck.owner].append(rank)

        model = PlackettLuce()

        possible_decks = []
        for person in persons_with_decks.keys():
            possible_decks.append(person_ranks[person])

        bab = itertools.product(*possible_decks)

        matches = []

        for pos in bab:
            teams = []
            # print("¤"*40)
            for p in pos:
                # print(p.name)
                teams.append([p])
            bab = model.predict_win(teams)
            hej = sum([abs(0.25 - b) for b in bab])
            # print(bab)
            # print(hej)

            matches.append((pos, hej, bab))

        matches.sort(key=lambda x: x[1])

        return matches


