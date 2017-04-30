# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from models import Temperature

logger = logging.getLogger(__name__)


# @register.filter
# def pdb(element):
#    import pdb; pdb.set_trace()
#    return element


class ListTemperatureView(ListView):
    model = Temperature
    template_name = u'temperature_list.html'
    paginate_by = 20
    object_list = None

    def get_context_data(self, **kwargs):

        context = super(ListTemperatureView, self).get_context_data(**kwargs)

        context[u'readings'] = len(self.object_list)

        #
        # Termperature
        maxTemperature, maxReadingDateTime, maxTemperatureID = self.get_maxTemperature(self.object_list)
        context[u'maxTemperature'] = u"%s on %s" % (maxTemperature, maxReadingDateTime)
        context[u'maxTemperatureID'] = maxTemperatureID

        minTemperature, minReadingDateTime, minTemperatureID = self.get_minTemperature(self.object_list)
        context[u'minTemperature'] = u"%s on %s" % (minTemperature, minReadingDateTime)
        context[u'minTemperatureID'] = minTemperatureID

        #
        # Humidity
        #
        maxHumidity, maxReadingDateTime, maxHumidityID = self.get_maxHumidity(self.object_list)
        context[u'maxHumidity'] = u"%s on %s" % (maxHumidity, maxReadingDateTime)
        context[u'maxHumidityID'] = maxHumidityID

        minHumidity, minReadingDateTime, minHumidityID = self.get_minHumidity(self.object_list)
        context[u'minHumidity'] = u"%s on %s" % (minHumidity, minReadingDateTime)
        context[u'minHumidityID'] = minHumidityID

        self.object_list = list([x for x in context[u'object_list'] if "temperature" in context[u'object_list']])
        # self.object_list = context[u'object_list']

        return context

    @staticmethod
    def get_minTemperature(object_list):

        minTemperature = 200.0
        minReadingDateTime = None
        minTemperatureID = None

        for x in object_list:
            tempF = float(x.TempF[:-2])

            if tempF < minTemperature:
                minTemperature = tempF
                minReadingDateTime = x.ReadingDateTime
                minTemperatureID = x.id

        return minTemperature, minReadingDateTime, minTemperatureID

    @staticmethod
    def get_maxTemperature(object_list):

        maxTemperature = 0.0
        maxReadingDateTime = None
        maxTemperatureID = None

        for x in object_list:
            tempF = float(x.TempF[:-2])

            if tempF > maxTemperature:
                maxTemperature = tempF
                maxReadingDateTime = x.ReadingDateTime
                maxTemperatureID = x.id

        return maxTemperature, maxReadingDateTime, maxTemperatureID

    #
    # Humidity
    #
    @staticmethod
    def get_minHumidity(object_list):

        minHumidity = 100.0
        minReadingDateTime = None
        minHumidityID = None

        for x in object_list:
            humidity = float(x.Humidity[:-1])

            logger.debug(u"Max Humidity : %d - %d" % (humidity, minHumidity))

            if humidity < minHumidity:
                minHumidity = humidity
                minReadingDateTime = x.ReadingDateTime
                minHumidityID = x.id

        return minHumidity, minReadingDateTime, minHumidityID

    @staticmethod
    def get_maxHumidity(object_list):

        maxHumidity = 0
        maxReadingDateTime = None
        maxHumidityID = None

        for x in object_list:
            humidity = float(x.Humidity[:-1])

            logger.debug(u"Max Humidity : %d - %d" % (humidity, maxHumidity))

            if humidity > maxHumidity:
                maxHumidity = humidity
                maxReadingDateTime = x.ReadingDateTime
                maxHumidityID = x.id

        return maxHumidity, maxReadingDateTime, maxHumidityID


class CreateTemperatureView(CreateView):
    model = Temperature
    template_name = u'temperature_edit.html'

    def get_success_url(self):
        return reverse(u'temperature_list')

    def get_context_data(self, **kwargs):
        context = super(CreateTemperatureView, self).get_context_data(**kwargs)

        context[u'action'] = reverse(u'temperature_new')

        return context


class EditTemperatureView(UpdateView):
    model = Temperature
    fields = u"__all__"

    template_name = u'temperature_edit.html'

    def get_success_url(self):
        return reverse(u'temperature_list')

    def get_context_data(self, **kwargs):
        context = super(EditTemperatureView, self).get_context_data(**kwargs)

        context[u'action'] = reverse(u'temperature_edit', kwargs={u'pk': self.get_object().id})

        return context


class DeleteTemperatureView(DeleteView):
    model = Temperature
    template_name = u'temperature_delete.html'

    def get_success_url(self):
        tr = reverse(u'temperature_list')
        return tr


class TemperatureView(DetailView):
    model = Temperature
    template_name = u'temperature.html'
    fields = u"__all__"
