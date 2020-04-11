from django.db import models


class Ongs(models.Model):
    nome = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    whatsapp = models.CharField(max_length=15)
    cidade = models.CharField(max_length=15)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return self.nome

class Incidents(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    value = models.FloatField()
    ong = models.ForeignKey(Ongs, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
