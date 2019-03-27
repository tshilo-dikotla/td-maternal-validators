from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator
from .form_validator_mixin import TDFormValidatorMixin


class AntenatalVisitMembershipFormValidator(TDCRFFormValidator,
                                            TDFormValidatorMixin, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()

        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))
