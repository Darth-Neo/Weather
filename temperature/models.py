# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models


class Temperature(models.Model):
    ReadingDateTime = models.CharField(max_length=255, )
    TempF = models.CharField(max_length=255, )
    Humidity = models.CharField(max_length=255, )
    id = None

    class Meta:
        ordering = [u"-id"]

    def __str__(self):
        return u"%s %s %s" % (self.ReadingDateTime, self.TempF, self.Humidity, )

    def get_absolute_url(self):
        return reverse(u'temperature_view', kwargs={u'pk': self.id})
