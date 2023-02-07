from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('matches', views.matches, name='matches'),
    path('decks', views.decks, name='decks'),
    path('stats', views.stats, name='stats'),
]
