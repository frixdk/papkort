from openskill.models import PlackettLuce

from ..models import Match, Deck


class GameService:
    @staticmethod
    def calculate_deck_rankings():
        # Calculate deck rankings
        matches = Match.objects.order_by('id').prefetch_related('players', 'players__person', 'players__deck')
        decks = Deck.objects.all()
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
