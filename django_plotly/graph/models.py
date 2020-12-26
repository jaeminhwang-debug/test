import pytz
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class BinStruct(models.Model):
    label = models.CharField(max_length=256)
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = self.modified = timezone.now()
        else:
            self.modified = timezone.now()
        return super().save(*args, **kwargs)

class BinField(models.Model):
    bs = models.ForeignKey(BinStruct, on_delete=models.CASCADE, blank=True)
    label = models.CharField(max_length=256, blank=True)
    bits = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.id) + ':' + self.bs.label + '.' + self.label + '(' + str(self.bits) + ')'

    def clean(self):
        if (self.bits is None) or (self.bits < 1) or (64 < self.bits):
            raise ValidationError('bits must be in 1 to 64')

class BinData(models.Model):
    file = models.FileField(blank=True, upload_to=settings.UPLOAD_ROOT + '%Y/%m/%d/')
    fname = models.CharField(max_length=256, blank=True)
    uploaded = models.DateTimeField(blank=True)

    def __str__(self):
        lt = self.uploaded.astimezone(pytz.timezone(settings.TIME_ZONE))
        lt_str = '{}({}-{}-{} {}:{}:{})'.format(self.fname,
            lt.year, lt.month, lt.day,
            lt.hour, lt.minute, lt.second)
        return lt_str

    def save(self, *args, **kwargs):
        self.uploaded = timezone.now()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
