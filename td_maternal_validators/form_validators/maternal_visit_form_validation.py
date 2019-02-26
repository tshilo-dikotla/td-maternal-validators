from django import forms
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_visit_tracking.form_validators import VisitFormValidator
from .form_validator_mixin import TDFormValidatorMixin


class MaternalVisitFormValidator(VisitFormValidator, TDFormValidatorMixin,
                                 FormValidator):

    def clean(self):
        condition = True if self.cleaned_data['survival_status'] == 'alive' \
            or self.cleaned_data['survival_status'] == 'dead' else False
        self.required_if_true(
            condition=condition,
            field_required='last_alive_date'
        )
        self.validate_against_consent_datetime(self.cleaned_data.get('report_datetime'))
        VisitFormValidator.clean(self)

    def validate_against_consent(self):
        """Returns an instance of the current maternal consent version form or
        raises an exception if not found."""
        try:
            self.consent_version_cls.objects.get(
                screening_identifier=self.subject_screening.screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Please complete mother\'s consent version form before proceeding')
        else:
            try:
                latest_consent = self.maternal_consent_cls.objects.get(
                    subject_identifier=self.cleaned_data.get('appointment').subject_identifier)
            except self.maternal_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Please complete Maternal Consent form '
                    f'before  proceeding.')
            else:
                return latest_consent

    @property
    def subject_screening(self):
        cleaned_data = self.cleaned_data
        try:
            return self.subject_screening_cls.objects.get(
                subject_identifier=cleaned_data['appointment'].subject_identifier)
        except self.subject_screening_cls.DoesNotExist:
            return None
