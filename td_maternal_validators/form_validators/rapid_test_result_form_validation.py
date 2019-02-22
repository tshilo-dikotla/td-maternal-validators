from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator


class RapidTestResultFormValidator(FormValidator):

    def clean(self):

        if self.cleaned_data.get('rapid_test_done') == YES:
            if not self.cleaned_data.get('result_date'):
                msg = {'result_date':
                       'This field is required'}
                self._errors.update(msg)
                raise ValidationError(msg)
            if not self.cleaned_data.get('result'):
                msg = {'result':
                       'This field is required'}
                self._errors.update(msg)
                raise ValidationError(msg)
        else:
            if self.cleaned_data.get('result_date'):
                msg = {'result_date':
                       'This field is not required'}
                self._errors.update(msg)
                raise ValidationError(msg)
            if self.cleaned_data.get('result'):
                msg = {'result':
                       'This field is not required'}
                self._errors.update(msg)
                raise ValidationError(msg)
