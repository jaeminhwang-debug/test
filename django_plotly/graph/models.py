from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class BinStructure(models.Model):
    name = models.CharField(max_length=256)
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = self.modified = timezone.now()
        else:
            self.modified = timezone.now()
        return super().save(*args, **kwargs)

class BinField(models.Model):
    bs = models.ForeignKey(BinStructure, on_delete=models.CASCADE)
    label = models.CharField(max_length=256, blank=True)
    bits = models.IntegerField(blank=True)

    def __str__(self):
        return "<BinField> label: '" + self.label + "', bits: " + str(self.bits)

    # def clean(self):
    #     if (self.bits is None) or (self.bits < 1) or (64 < self.bits):
    #         raise ValidationError('bits must be in 1 to 64')
