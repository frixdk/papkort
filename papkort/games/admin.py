from django.contrib import admin
from django.contrib.admin.options import StackedInline

from .models import Deck, Match, Person, Player


class DeckAdmin(admin.ModelAdmin):
    pass


class PlayerInline(StackedInline):
    extra = 4
    model = Player


class MatchAdmin(admin.ModelAdmin):
    inlines = (PlayerInline,)


class PersonAdmin(admin.ModelAdmin):
    pass


class PlayerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Deck, DeckAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Player, PlayerAdmin)

