from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('matches', views.matches, name='matches'),
    path('players', views.players, name='players'),
    path('decks', views.decks, name='decks'),
    path('stats', views.stats, name='stats'),
]
