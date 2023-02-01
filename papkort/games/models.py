from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

class Deck(models.Model):
    class Color(models.TextChoices):
        WHITE = 'w', _('White')
        BLUE = 'u', _('Blue')
        BLACK = 'b', _('Black')
        RED = 'r', _('Red')
        GREEN = 'g', _('Green')
        COLORLESS = 'colorless', _('Colorless')

        AZORIUS = 'wu', _('Azorius')
        DIMIR = 'ub', _('Dimir')
        RAKDOS = 'br', _('Rakdos')
        GRUUL = 'rg', _('Gruul')
        SELESNYA = 'gw', _('Selesnya')
        ORZHOV = 'wb', _('Orzhov')
        IZZET = 'ur', _('Izzet')
        GOLGARI = 'bg', _('Golgari')
        BOROS = 'rw', _('Boros')
        SIMIC = 'gu', _('Simic')

        ESPER = 'wub', _('Esper')
        GRIXIS = 'ubr', _('Grixis')
        JUND = 'brg', _('Jund')
        NAYA = 'rgw', _('Naya')
        BANT = 'gwu', _('Bant')
        ABZAN = 'wbg', _('Abzan')
        JESKAI = 'urw', _('Jeskai')
        SULTAI = 'bgu', _('Sultai')
        MARDU = 'rwb', _('Mardu (rwb)')
        TEMUR = 'gur', _('Temur')

        YORE_TILLER = 'wubr', _('Yore-Tiller')
        GLINT_EYE = 'ubrg', _('Glint-Eye')
        DUNE_BROOD = 'brgw', _('Dune-Brood')
        INK_TREADER = 'rgwu', _('Ink-Treader')
        WITCH_MAW = 'gwub', _('Witch-Maw')
        FIVE_COLOR = 'wubrg', _('Five Color')

    name = models.CharField(max_length=64, blank=True, null=True)
    commander = models.CharField(max_length=64)
    color = models.CharField(
        choices=Color.choices,
        max_length=16
    )
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        if self.name:
            return f'{self.name} ({self.commander})'
        else:
            return self.commander


class Match(models.Model):
    class Meta:
        verbose_name_plural = 'matches'

    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def winner(self) -> list['Player']:
        return self.players.filter(position=1)

    def __str__(self):
        return f'{self.date} - {", ".join([p.person.name for p in self.players.all()])} - ({", ".join([w.person.name for w in self.winner()])} won)'

class Player(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    deck = models.ForeignKey(Deck, on_delete=models.PROTECT)
    position = models.IntegerField()
    match = models.ForeignKey(Match, related_name='players', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.person.name} ranked {self.position} with {self.deck}'



