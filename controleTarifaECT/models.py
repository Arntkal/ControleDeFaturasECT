from django.db import models

# Create your models here.
class CodigoTarifa(models.Model):
    codigoECT = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):              # __unicode__ on Python 2
        return self.codigoECT
    
class Tarifa(models.Model):
    idCodigoTarifa = models.ForeignKey(CodigoTarifa, on_delete=models.PROTECT)
    peso_I = models.IntegerField()
    peso_F = models.IntegerField()
    rangeL1 = models.CharField(max_length=20)
    rangeL2 = models.CharField(max_length=20)
    rangeL3 = models.CharField(max_length=20)
    rangeL4 = models.CharField(max_length=20)
    rangeE1 = models.CharField(max_length=20)
    rangeE2 = models.CharField(max_length=20)
    rangeE3 = models.CharField(max_length=20)
    rangeE4 = models.CharField(max_length=20)
    rangeN1 = models.CharField(max_length=20)
    rangeN2 = models.CharField(max_length=20)
    rangeN3 = models.CharField(max_length=20)
    rangeN4 = models.CharField(max_length=20)
    rangeN5 = models.CharField(max_length=20)    
    rangeN6 = models.CharField(max_length=20)
    rangeI1 = models.CharField(max_length=20)
    rangeI2 = models.CharField(max_length=20)
    rangeI3 = models.CharField(max_length=20)
    rangeI4 = models.CharField(max_length=20)
    rangeI5 = models.CharField(max_length=20)
    rangeI6 = models.CharField(max_length=20)

    def __str__(self):              # __unicode__ on Python 2
        return f"codEct : {self.idCodigoTarifa}, Peso: de {self.peso_I}gr a {self.peso_F}gr "