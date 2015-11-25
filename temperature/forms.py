#!/usr/bin/env python
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from models import Temperature


class TemperatureForm(forms.ModelForm):
    confirm_email = forms.EmailField(
        label=u"Confirm email",
        required=True,
    )

    class Meta:
        model = Temperature

    def __init__(self, *args, **kwargs):

        if kwargs.get(u'instance'):
            email = kwargs[u'instance'].email
            kwargs.setdefault(u'initial', {})[u'confirm_email'] = email

        super(TemperatureForm, self).__init__(*args, **kwargs)

    def clean(self):

        if (self.cleaned_data.get(u'email') !=
                self.cleaned_data.get(u'confirm_email')):
            raise ValidationError(
                u"Email addresses must match."
            )

        return self.cleaned_data


# inlineformset_factory creates a Class from a parent model (Contact)
# to a child model (Address)
TemperatureFormSet = inlineformset_factory(
    Temperature
)
