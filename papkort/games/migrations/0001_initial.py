# Generated by Django 4.1.5 on 2023-01-31 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('commander', models.CharField(max_length=64)),
                ('color', models.CharField(choices=[('w', 'White'), ('u', 'Blue'), ('b', 'Black'), ('r', 'Red'), ('g', 'Green'), ('colorless', 'Colorless'), ('wu', 'Azorius'), ('ub', 'Dimir'), ('br', 'Rakdos'), ('rg', 'Gruul'), ('gw', 'Selesnya'), ('wb', 'Orzhov'), ('ur', 'Izzet'), ('bg', 'Golgari'), ('rw', 'Boros'), ('gu', 'Simic'), ('wub', 'Esper'), ('ubr', 'Grixis'), ('brg', 'Jund'), ('rgw', 'Naya'), ('gwu', 'Bant'), ('wbg', 'Abzan'), ('urw', 'Jeskai'), ('bgu', 'Sultai'), ('rwb', 'Mardu (rwb)'), ('gur', 'Temur'), ('wubr', 'Yore-Tiller'), ('ubrg', 'Glint-Eye'), ('brgw', 'Dune-Brood'), ('rgwu', 'Ink-Treader'), ('gwub', 'Witch-Maw'), ('wubrg', 'Five Color')], max_length=16)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'matches',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='games.deck')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='players', to='games.match')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='games.person')),
            ],
        ),
    ]
