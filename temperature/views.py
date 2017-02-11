from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import ListView

from django.core.urlresolvers import reverse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView

from django.db.models import Max
from django.db.models import Min
from models import Temperature

import logging
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

        """
        min_TempF = Temperature.objects.all().aggregate(Min(u'TempF'))
        temperature = Temperature.objects.all().filter(TempF = min_TempF)
        minReadingDateTime = temperature.ReadingDateTime

        Temperature.objects.filter(ReadingDateTime='Sales').values('dept_name').annotate(Count('employee'))
        Temperature.objects.filter(dept_name='Sales').aggregate(Count('employee'))
        """

        if False:
            minTemperature = Temperature.objects.all().aggregate(Min(u'TempF'))
            temperature = Temperature.objects.get(TempF=minTemperature)
            minReadingDateTime = temperature.ReadingDateTime
            context[u'minTemperature'] = u"%s on %s" % (minTemperature, minReadingDateTime)
            context[u'minTemperatureID'] = temperature.ID

            maxTemperature = Temperature.objects.all().aggregate(Max(u'TempF'))
            temperature = Temperature.objects.all().filter(TempF=maxTemperature)
            maxReadingDateTime = temperature.ReadingDateTime
            context[u'maxTemperature'] = u"%s on %s" % (maxTemperature, maxReadingDateTime)
            context[u'maxTemperatureID'] = temperature.ID

            max_TempF = Temperature.objects.all().aggregate(Max(u'TempF'))
            min_TempF = Temperature.objects.all().aggregate(Min(u'TempF'))

            max_Humidity = Temperature.objects.all().aggregate(Max(u'Humidity'))
            min_Humidity = Temperature.objects.all().aggregate(Min(u'Humidity'))

            max_Barometer = Temperature.objects.all().aggregate(Max(u'Barometer'))
            min_Barometer = Temperature.objects.all().aggregate(Min(u'Barometer'))
        else:
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

            #
            # Barometer
            #
            maxBarometer, maxReadingDateTime, maxBarometerID = self.get_maxBarometer(self.object_list)
            context[u'maxBarometer'] = u"%s on %s" % (maxBarometer, maxReadingDateTime)
            context[u'maxBarometerID'] = maxBarometerID

            minBarometer, minReadingDateTime, minBarometerID = self.get_minBarometer(self.object_list)
            context[u'minBarometer'] = u"%s on %s" % (minBarometer, minReadingDateTime)
            context[u'minBarometerID'] = minBarometerID

        self.object_list = context[u'object_list']

        return context

    def get_minTemperature(self, object_list):

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

    def get_maxTemperature(self, object_list):

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
    def get_minHumidity(self, object_list):

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

    def get_maxHumidity(self, object_list):

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

    #
    # Barometer
    #
    def get_minBarometer(self, object_list):

        minBarometer = 1000.0
        minReadingDateTime = None
        minBarometerID = None

        for x in object_list:

            try:
                barometer = float(x.Barometer)
            except:
                continue

            logger.debug(u"Max Barometer : %d - %d" % (barometer, minBarometer))

            if barometer < minBarometer:
                minBarometer = barometer
                minReadingDateTime = x.ReadingDateTime
                minBarometerID = x.id

        return minBarometer, minReadingDateTime, minBarometerID

    def get_maxBarometer(self, object_list):

        maxBarometer = 0.0
        maxReadingDateTime = None
        maxBarometerID = None

        for x in object_list:
            try:
                barometer = float(x.Barometer)
            except:
                continue

            logger.debug(u"Max Barometer : %d - %d" % (barometer, maxBarometer))

            if barometer > maxBarometer:
                maxBarometer = barometer
                maxReadingDateTime = x.ReadingDateTime
                maxBarometerID = x.id

        return maxBarometer, maxReadingDateTime, maxBarometerID


class CreateTemperatureView(CreateView):

    model = Temperature
    template_name = u'temperature_edit.html'

    def get_success_url(self):
        return reverse(u'temperature_list')

    def get_context_data(self, **kwargs):

        context = super(CreateTemperatureView, self).get_context_data(**kwargs)

        context[u'action'] = reverse(u'temperature_new')

        return context


class UpdateTemperatureView(UpdateView):

    model = Temperature
    fields = u"__all__"
    
    template_name = u'temperature_edit.html'

    def get_success_url(self):
        return reverse(u'temperature_list')
  
    def get_context_data(self, **kwargs):

        context = super(UpdateTemperatureView, self).get_context_data(**kwargs)

        context[u'action'] = reverse(u'temperature_edit', kwargs={u'pk': self.get_object().id})

        return context


class DeleteTemperatureView(DeleteView):

    model = Temperature
    template_name = u'temperature_delete.html'

    def get_success_url(self):
        return reverse(u'temperature_list')


class TemperatureView(DetailView):

    model = Temperature
    template_name = u'temperature.html'
