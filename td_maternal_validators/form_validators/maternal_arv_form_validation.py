from django import forms
from edc_form_validators import FormValidator
from django.core.exceptions import ValidationError
from edc_constants.constants import YES


class MaternalArvFormValidator(FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stop_date') < cleaned_data.get('start_date'):
            msg = {'start_date': 'Your stop date of {} is prior to start date of {}.'
                   'Please correct'
                   .format(cleaned_data.get('stop_date'),
                           cleaned_data.get('start_date'))}
            self._errors.update(msg)
            raise ValidationError(msg)

        condition = (self.cleaned_data.get('maternal_arv_preg').took_arv == YES and
                     not self.cleaned_data.get('arv_code'))
        if condition:
            msg = {'arv_code': 'You indicated that participant started ARV(s) during'
                   'this pregnancy. Please list them on maternal_arv table.'
                   }
            self._errors.update(msg)
            raise forms.ValidationError(msg)
        if self.cleaned_data.get('arv_history'):
            haart_start_date = self.cleaned_data.get(
                'arv_history').haart_start_date

            if cleaned_data.get('start_date') < haart_start_date:
                msg = {'start_date': 'Your ARV start date {} in this pregnancy cannot'
                       'be before your historical ARV date {}'
                       .format(cleaned_data.get('start_date'),
                               haart_start_date)
                       }
                self._errors.update(msg)
                raise ValidationError(msg)

        if self.cleaned_data.get('stop_date'):
            if not self.cleaned_data.get('reason_for_stop'):
                msg = {'reason_for_stop': 'ARV stopped, please give reason for stop.'}
                self._errors.update(msg)
                raise forms.ValidationError(msg)
