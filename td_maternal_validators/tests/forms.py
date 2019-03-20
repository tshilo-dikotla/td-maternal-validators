from django import forms
from django.core.exceptions import ValidationError

from ..form_validators import MaternalArvFormValidator

from .models import MaternalArv


class MaternalArvForm(forms.ModelForm):

    form_validator_cls = MaternalArvFormValidator
    errors = {}

    class Meta:
        model = MaternalArv
        fields = '__all__'

    def clean(self):
        self.validate_num_arvs()

    def validate_num_arvs(self):
        maternal_arv = self.data.get(
            'maternalarv_set-2-arv_code')
        print(maternal_arv)
        if not maternal_arv:
            message = {'arv_code':
                       'Patient should have more than 3 arvs'
                       }
            print('****************************************')
            self.errors.update(message)
            raise ValidationError(message)

    def validate_date_arv_stopped(self):
        maternal_arv = self.data.get(
            'maternalarv_set-0-stop_date')
        maternal_arv = self.data.get(
            'maternalarv_set-1-stop_date')
        maternal_arv = self.data.get(
            'maternalarv_set-2-stop_date')
        
