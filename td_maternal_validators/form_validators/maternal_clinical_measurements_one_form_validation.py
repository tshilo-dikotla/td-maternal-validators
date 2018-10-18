from edc_form_validators import FormValidator
from django.core.exceptions import ValidationError


class MaternalClinicalMeasurememtsOneFormValidator(FormValidator):
    def clean(self):
        if not self.cleaned_data.get('systolic_bp') \
                and not self.cleaned_data.get('diastolic_bp'):
            msg = {'systolic_bp': 'systolic_bp Blood Pressure'
                                  'field cannot be blank.'
                                  'Please correct',
                   'diastolic_bp': 'diastolic_bp Blood'
                                   'Pressure field cannot be blank.'
                                   'Please correct'}

            self._errors.update(msg)
            raise ValidationError(msg)

        cleaned_data = self.cleaned_data
        if cleaned_data.get('systolic_bp') < \
                cleaned_data.get('diastolic_bp'):
            msg = {'diastolic_bp': 'Systolic_bp blood pressure cannot be lower'
                                   'than the diastolic_bp blood pressure.'
                                   'Please correct.'}
            self._errors.update(msg)
            raise ValidationError(msg)
