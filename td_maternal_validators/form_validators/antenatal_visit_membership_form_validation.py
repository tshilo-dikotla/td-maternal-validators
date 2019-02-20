from edc_form_validators import FormValidator

from .form_validator_mixin import TDFormValidatorMixin


class AntenatalVisitMembershipFormValidator(TDFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))
