# Generated by Django 3.2.2 on 2021-12-01 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DistanciasPracas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_inicial', models.IntegerField(verbose_name='ID inicial')),
                ('id_final', models.IntegerField(verbose_name='ID final')),
                ('distancia', models.FloatField(verbose_name='Distancia')),
            ],
        ),
    ]
