from django.db import models

# Create your models here.
# class BinStructure(models.Model):
#     name = models.CharField(max_length=256)

class BinField(models.Model):
    bin_structure = models.ForeignKey(BinStructure, on_delete=models.CASCADE)
    label = models.CharField(max_length=256)
    bits = models.IntegerField()
