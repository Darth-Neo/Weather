from django.db import models
from django.core.urlresolvers import reverse


class Temperature(models.Model):
    ReadingDateTime = models.CharField(max_length=255, )
    TempF = models.CharField(max_length=255, )
    Humidity = models.CharField(max_length=255, )
    Barometer = models.CharField(max_length=255, )

    class Meta:
        ordering = [u"-id"]

    def __str__(self):
        return u"%s %s %s %s" % (self.ReadingDateTime, self.TempF, self.Humidity, self.Barometer, )

    def get_absolute_url(self):
        return reverse(u'temperature_view', kwargs={u'pk': self.id})
