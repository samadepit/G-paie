from django.db import models

class Task(models.Model):
    Nom = models.CharField(max_length=255)
    Prix = models.DecimalField(max_digits=8,decimal_places=2)
    Quantité = models.IntegerField()
    Date_de_peremption = models.DateTimeField()
# Create your models here.
