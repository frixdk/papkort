from django.contrib import admin
from django.contrib.admin.options import StackedInline

from .models import Deck, Match, Person, Player


class DeckAdmin(admin.ModelAdmin):
    list_display = ("commander", "name", "owner", "color", "get_win_percentage")
    search_fields = ["commander", "name"]
    ordering = ["commander"]


class PlayerInline(StackedInline):
    extra = 4
    model = Player
    autocomplete_fields = ["deck"]


class MatchAdmin(admin.ModelAdmin):
    inlines = (PlayerInline,)


class PersonAdmin(admin.ModelAdmin):
    ordering = ["name"]


class PlayerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Deck, DeckAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Player, PlayerAdmin)

