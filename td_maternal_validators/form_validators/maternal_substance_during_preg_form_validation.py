from edc_constants.constants import YES
from edc_form_validators.form_validator import FormValidator

from .crf_form_validator import TDCRFFormValidator


class MaternalSubstanceUseDuringPregFormValidator(TDCRFFormValidator,
                                                  FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        required_fields = {'smoked_during_pregnancy': 'smoking_during_preg_freq',
                           'alcohol_during_pregnancy': 'alcohol_during_preg_freq',
                           'marijuana_during_preg': 'marijuana_during_preg_freq'
                           }

        for field, required_field in required_fields.items():
            self.required_if(
                YES,
                field=field,
                field_required=required_field,
                required_msg='please give a frequency.',
                not_required_msg='please do not give a frequency.'
            )
