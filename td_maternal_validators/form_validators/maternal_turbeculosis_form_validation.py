from django import forms
from edc_form_validators import FormValidator
from django.core.exceptions import ValidationError
from edc_constants.constants import YES


class MaternalTuberculosisHistoryFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='coughing',
            field_required='coughing_relation'
        ),

        self.required_if(
            YES,
            field='diagnosis',
            field_required='diagnosis_relation'
        ),

        self.required_if(
            YES,
            field='tuberculosis_treatment',
            field_required='tuberculosis_treatment_relation'
        )