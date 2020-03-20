from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import TDCRFFormValidator


class MaternalArvPregFormValidator(TDCRFFormValidator, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.applicable_if(
            YES,
            field='is_interrupt',
            field_applicable='interrupt',
        )

        self.validate_other_specify(
            field='interrupt',
            other_specify_field='interrupt_other',
            required_msg='Please give reason for interruption'
        )
