from edc_form_validators import FormValidator
from django.core.exceptions import ValidationError


class MaternalClinicalMeasurememtsOneFormValidator(FormValidator):
    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('systolic_bp') < \
                cleaned_data.get('diastolic_bp'):
            msg = {'diastolic_bp': 'Systolic blood pressure cannot be lower '
                                   'than the diastolic blood pressure. '
                                   'Please correct.'}
            self._errors.update(msg)
            raise ValidationError(msg)
