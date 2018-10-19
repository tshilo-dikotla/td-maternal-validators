from edc_form_validators import FormValidator
from django.core.exceptions import ValidationError
from edc_constants.constants import YES


class MaternalArvFormValidator(FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stop_date') < cleaned_data.get('start_date'):
            msg = {'start_date': 'Your stop date of {} is prior'
                                 'to start date of {}. Please'
                                 'correct'
                                 .format(cleaned_data.get('stop_date'),
                                         cleaned_data.get('start_date'))}
            self._errors.update(msg)
            raise ValidationError(msg)

        #condition = cleaned_data.get('maternal_arv_preg').took_arv == YES
       # self.required_if_true(condition, )