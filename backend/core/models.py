"""Models all project."""
from django.db import models


class ONGs(models.Model):
    """Models to create ONGs."""

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    whatsapp = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    uf = models.CharField(max_length=2)

    def __str__(self):
        """Representation in the model."""
        return self.name


class Incidents(models.Model):
    """Models to create incidents."""

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    value = models.FloatField()
    ong = models.ForeignKey(ONGs, on_delete=models.CASCADE)

    def __str__(self):
        """Representation in the model."""
        return self.title
