from edc_form_validators import FormValidator

from .form_validator_mixin import TDFormValidatorMixin


class TDConsentVersionFormValidator(TDFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_consent()

    @property
    def subject_screening(self):
        cleaned_data = self.cleaned_data
        try:
            return self.subject_screening_cls.objects.get(
                screening_identifier=cleaned_data.get('screening_identifier'))
        except self.subject_screening_cls.DoesNotExist:
            return None
