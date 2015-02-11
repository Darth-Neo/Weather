from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import ListView

from django.core.urlresolvers import reverse

from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView

from temperature.models import Temperature

class ListTemperatureView(ListView):
    model = Temperature
    template_name = 'temperature_list.html'

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
