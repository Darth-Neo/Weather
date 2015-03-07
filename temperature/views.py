from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import ListView

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView

from temperature.models import Temperature

#@register.filter
#def pdb(element):
#    import pdb; pdb.set_trace()
#    return element

class ListTemperatureView(ListView):

    model = Temperature
    template_name = 'temperature_list.html'
    paginate_by = 25
    object_list = None

    def get_context_data(self, **kwargs):

        context = super(ListTemperatureView, self).get_context_data(**kwargs)

        context['readings'] = len(self.object_list)

        maxTemperature, maxReadingDateTime = self.get_maxTemperature(self.object_list)
        context['maxTemperature'] = "%s on %s" % (maxTemperature, maxReadingDateTime)

        minTemperature, minReadingDateTime = self.get_minTemperature(self.object_list)
        context['minTemperature'] = "%s on %s" % (minTemperature, minReadingDateTime)

        maxHumidity, maxReadingDateTime = self.get_maxHumidity(self.object_list)
        context['maxHumidity'] = "%s on %s" % (maxHumidity, maxReadingDateTime)

        minHumidity, minReadingDateTime = self.get_minHumidity(self.object_list)
        context['minHumidity'] = "%s on %s" % (minHumidity, minReadingDateTime)


        self.object_list = context['object_list']

        return context

    def get_minTemperature(self, object_list):

        minTemperature = 200.0
        minReadingDateTime = None

        for x in object_list:
            tempF = float(x.TempF[:-2])

            if tempF < minTemperature:
                minTemperature = tempF
                minReadingDateTime = x.ReadingDateTime

        return minTemperature, minReadingDateTime

    def get_maxTemperature(self, object_list):

        maxTemperature  = 0.0
        maxReadingDateTime = None

        for x in object_list:
            tempF = float(x.TempF[:-2])

            if tempF > maxTemperature:
                maxTemperature = tempF
                maxReadingDateTime = x.ReadingDateTime

        return maxTemperature, maxReadingDateTime

    #
    # Humidity
    #
    def get_minHumidity(self, object_list):

        minHumidity = 200.0
        minReadingDateTime = None

        for x in object_list:
            humidity = float(x.Humidity[:-1])

            if humidity < minHumidity:
                minHumidity = humidity
                minReadingDateTime = x.ReadingDateTime

        return minHumidity, minReadingDateTime

    def get_maxHumidity(self, object_list):

        maxHumidity  = 0.0
        maxReadingDateTime = None

        for x in object_list:
            humidity = float(x.Humidity[:-1])

            if humidity > maxHumidity:
                maxHumidity = humidity
                maxReadingDateTime = x.ReadingDateTime

        return maxHumidity, maxReadingDateTime

class CreateTemperatureView(CreateView):

    model = Temperature
    template_name = 'temperature_edit.html'

    def get_success_url(self):
        return reverse('temperature_list')

    def get_context_data(self, **kwargs):

        context = super(CreateTemperatureView, self).get_context_data(**kwargs)

        context['action'] = reverse('temperature_new')

        return context

class UpdateTemperatureView(UpdateView):

    model = Temperature
    template_name = 'temperature_edit.html'

    def get_success_url(self):
        return reverse('temperature_list')
  
    def get_context_data(self, **kwargs):

        context = super(UpdateTemperatureView, self).get_context_data(**kwargs)

        context['action'] = reverse('temperature_edit',
                                    kwargs={'pk': self.get_object().id})

        return context

class DeleteTemperatureView(DeleteView):

    model = Temperature
    template_name = 'temperature_delete.html'

    def get_success_url(self):
        return reverse('temperature_list')

class TemperatureView(DetailView):

    model = Temperature
    template_name = 'temperature.html'
