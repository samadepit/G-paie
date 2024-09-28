from django.db import models

class Task(models.Model):
    Nom = models.CharField(max_length=255)
    Prix = models.DecimalField(max_digits=8,decimal_places=2)
    Quantite = models.IntegerField()
    Date_de_peremption = models.DateTimeField()
class Paiement(models.Model):
    Nom = models.CharField(max_length=255)
    Prix = models.DecimalField(max_digits=8,decimal_places=2)
    Quantite = models.IntegerField()
    Date_of_buy = models.DateTimeField()
# Create your models here.
