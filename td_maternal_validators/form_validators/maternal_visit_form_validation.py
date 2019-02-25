from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_visit_tracking.form_validators import VisitFormValidator


class MaternalVisitFormValidator(VisitFormValidator, FormValidator):

    def clean(self):
        last_alive_date = self.cleaned_data['last_alive_date']
        if not last_alive_date:
            msg = {'last_alive_date': 'This field is required'}
            raise ValidationError(msg)
        VisitFormValidator.clean(self)
