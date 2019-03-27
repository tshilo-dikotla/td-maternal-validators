from django import forms
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator
from .form_validator_mixin import TDFormValidatorMixin


class TDConsentVersionFormValidator(TDCRFFormValidator,
                                    TDFormValidatorMixin, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()

        self.validate_against_screening_datetime(
            self.cleaned_data.get('report_datetime'))

    def validate_against_screening_datetime(self, report_datetime):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""

        if report_datetime < self.subject_screening.report_datetime:
            raise forms.ValidationError(
                "Report datetime cannot be before screening datetime")

    @property
    def subject_screening(self):
        cleaned_data = self.cleaned_data
        try:
            return self.subject_screening_cls.objects.get(
                screening_identifier=cleaned_data.get('screening_identifier'))
        except self.subject_screening_cls.DoesNotExist:
            raise ValidationError(
                'Please complete Subject Screening form for version '
                f'before  proceeding.')
