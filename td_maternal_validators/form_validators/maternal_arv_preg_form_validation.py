from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .form_validator_mixin import TDFormValidatorMixin


class MaternalArvPregFormValidator(TDFormValidatorMixin, FormValidator):

    def clean(self):

        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'),
            self.cleaned_data.get('maternal_visit').subject_identifier)

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

    @property
    def subject_screening(self):
        cleaned_data = self.cleaned_data
        try:
            return self.subject_screening_cls.objects.get(
                subject_identifier=cleaned_data.get('maternal_visit').subject_identifier)
        except self.subject_screening_cls.DoesNotExist:
            return None
