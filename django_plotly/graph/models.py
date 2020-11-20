from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class BinStructure(models.Model):
    name = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return "<BinStructure> name: '" + self.name + "'"

class BinField(models.Model):
    bin_structure = models.ForeignKey(BinStructure, on_delete=models.CASCADE)
    label = models.CharField(max_length=256, blank=True)
    bits = models.IntegerField(blank=True)

    def __str__(self):
        return "<BinField> label: '" + self.label + "', bits: " + str(self.bits)

    # def clean(self):
    #     if (self.bits is None) or (self.bits < 1) or (64 < self.bits):
    #         raise ValidationError('bits must be in 1 to 64')
