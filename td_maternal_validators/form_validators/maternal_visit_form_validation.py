from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_action_item.site_action_items import site_action_items
from edc_constants.constants import OFF_STUDY, DEAD, YES, ON_STUDY, NO, NEW
from edc_form_validators import FormValidator
from edc_metadata.constants import NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import MISSED_VISIT, LOST_VISIT
from edc_visit_tracking.form_validators import VisitFormValidator

from td_maternal.action_items import MATERNALOFF_STUDY_ACTION
from td_maternal.action_items import MATERNAL_DEATH_REPORT_ACTION

from .crf_form_validator import TDCRFFormValidator
from .form_validator_mixin import TDFormValidatorMixin


class MaternalVisitFormValidator(VisitFormValidator, TDCRFFormValidator,
                                 TDFormValidatorMixin, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'appointment').subject_identifier
        super().clean()

        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))

        self.validate_study_status()

        self.validate_death()

        self.validate_reason()

        self.validate_last_alive_date()

    def validate_reason(self):

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

        self.required_if_true(
            reason == MISSED_VISIT,
            field_required='reason_missed'
        )

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

    def validate_study_status(self):
        maternal_offstudy_cls = django_apps.get_model(
            'td_maternal.maternaloffstudy')
        action_cls = site_action_items.get(
            maternal_offstudy_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                action_type__name=MATERNALOFF_STUDY_ACTION,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            try:
                maternal_offstudy_cls.objects.get(
                    subject_identifier=self.subject_identifier)
            except maternal_offstudy_cls.DoesNotExist:
                pass
            else:
                if self.cleaned_data.get('study_status') == ON_STUDY:
                    raise forms.ValidationError(
                        {'study_status': 'Participant has been taken offstudy.'
                         ' Cannot be indicated as on study.'})
        else:
            raise forms.ValidationError(
                {'study_status': 'Participant is scheduled to go offstudy.'
                 ' Cannot edit visit until offstudy form is completed.'})
