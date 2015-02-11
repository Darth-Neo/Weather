from django.db import models
from django.core.urlresolvers import reverse

class Temperature(models.Model):

    ReadingDateTime = models.CharField(max_length=255,)
    TempC = models.CharField(max_length=255,)
    TempF = models.CharField( max_length=255,)
    Humidity = models.CharField(max_length=255,)

    def __str__(self):

        return ' '.join([ self.ReadingDateTime, self.TempC, self.TempF, self.Humidity, ])

    def get_absolute_url(self):

        return reverse('temperature_view', kwargs={'pk': self.id})
