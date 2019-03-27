from django.core.exceptions import ValidationError
from edc_constants.constants import OFF_STUDY, DEAD, YES
from edc_form_validators import FormValidator
from edc_visit_tracking.constants import MISSED_VISIT, LOST_VISIT
from edc_visit_tracking.form_validators import VisitFormValidator

from .crf_form_validator import TDCRFFormValidator
from .form_validator_mixin import TDFormValidatorMixin


class MaternalVisitFormValidator(TDCRFFormValidator,
                                 TDFormValidatorMixin, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'appointment').subject_identifier
        super().clean()

        self.validate_death()

        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))

        is_present = self.cleaned_data.get('is_present')
        reason = self.cleaned_data.get('reason')
        if is_present and is_present == YES:
            if reason in [MISSED_VISIT, LOST_VISIT]:
                msg = {'reason': 'If Q9 is present, this field must not be '
                       'missed visit or lost visits'}
                self._errors.update(msg)
                raise ValidationError(msg)

        if (reason == LOST_VISIT and
                self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant has been lost to follow up, '
                   'study status should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        self.validate_last_alive_date()

    def validate_death(self):
        if (self.cleaned_data.get('survival_status') == DEAD
                and self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant is deceased, study status '
                   'should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_last_alive_date(self):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""

        latest_consent = self.validate_against_consent()
        last_alive_date = self.cleaned_data.get('last_alive_date')
        if last_alive_date and last_alive_date < latest_consent.consent_datetime.date():
            msg = {'last_alive_date': 'Date cannot be before consent date'}
            self._errors.update(msg)
            raise ValidationError(msg)
