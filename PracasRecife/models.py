from django.db import models

class DistanciasPracas(models.Model):
    id_inicial = models.IntegerField(verbose_name='ID inicial')
    id_final = models.IntegerField(verbose_name='ID final')
    distancia = models.FloatField(verbose_name='Distancia')


class Grafo(models.Model):
    grafo = models.TextField(verbose_name='Grafo')
