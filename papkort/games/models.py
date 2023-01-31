from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=64)


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
        MARDU = 'rwb', _('Mardu')
        TEMUR = 'gur', _('Temur')

        YORE_TILLER = 'wubr', _('Yore-Tiller')
        GLINT_EYE = 'ubrg', _('Glint-Eye')
        DUNE_BROOD = 'brgw', _('Dune-Brood')
        INK_TREADER = 'rgwu', _('Ink-Treader')
        WITCH_MAW = 'gwub', _('Witch-Maw')
        FIVE_COLOR = 'wubrg', _('Five Color')

    name = models.CharField(max_length=64)
    commander = models.CharField(max_length=64)
    color = models.CharField(
        choices=Color.choices,
        max_length=16
    )
    description = models.TextField()
    url = models.CharField(max_length=128)


class Player(models.Model):
    person = models.ForeignKey(Person)
    deck = models.ForeignKey(Deck)

    position integerfield


class Match(models.Model):
    - date
    - list of players. many to many
    - notes
