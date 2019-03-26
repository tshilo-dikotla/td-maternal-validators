from django.core.exceptions import ValidationError
from edc_constants.constants import OFF_STUDY, DEAD, YES
from edc_form_validators import FormValidator
from edc_visit_tracking.form_validators import VisitFormValidator
from edc_visit_tracking.constants import MISSED_VISIT, LOST_VISIT

from .form_validator_mixin import TDFormValidatorMixin


class MaternalVisitFormValidator(TDFormValidatorMixin, VisitFormValidator,
                                 FormValidator):

    def clean(self):
        super().clean()

        self.validate_death()

        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))

        is_present = self.cleaned_data.get('is_present')
        reason = self.cleaned_data.get('reason')
        if is_present and is_present == YES:
            if reason in [MISSED_VISIT, LOST_VISIT]:
                msg = 'if Q9 is present, this field must not be missed visit or lost visits'
                raise ValidationError(msg)
        self.validate_last_alive_date()

    def validate_death(self):
        if (self.cleaned_data.get('survival_status') == DEAD
                and self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant is deceased, study status '
                   'should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_against_consent(self):
        """Returns an instance of the current maternal consent version form or
        raises an exception if not found."""
        try:
            self.consent_version_cls.objects.get(
                screening_identifier=self.subject_screening.screening_identifier
            )
        except self.consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Please complete mother\'s consent version form before proceeding')
        else:
            try:
                latest_consent = self.maternal_consent_cls.objects.get(
                    subject_identifier=self.cleaned_data.get(
                        'appointment').subject_identifier)
            except self.maternal_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Please complete Maternal Consent form '
                    f'before  proceeding.')
            else:
                return latest_consent

    def validate_last_alive_date(self):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""

        latest_consent = self.validate_against_consent()
        last_alive_date = self.cleaned_data.get('last_alive_date')
        if last_alive_date and last_alive_date < latest_consent.consent_datetime.date():
            msg = {'last_alive_date': 'Date cannot be before consent date'}
            self._errors.update(msg)
            raise ValidationError(msg)

    @property
    def subject_screening(self):
        cleaned_data = self.cleaned_data
        try:
            return self.subject_screening_cls.objects.get(
                subject_identifier=cleaned_data.get('appointment').subject_identifier)
        except self.subject_screening_cls.DoesNotExist:
            return None
