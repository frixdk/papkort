from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('matches', views.matches, name='matches'),
    path('players', views.players, name='players'),
    path('person-stats/<int:person_id>/', views.person_stats, name='person_stats'),
    path('decks', views.decks, name='decks'),
    path('stats', views.stats, name='stats'),
    path('ranks', views.ranks, name='ranks'),
]
