from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import OFF_STUDY, DEAD, YES, ON_STUDY, NEW
from edc_constants.constants import PARTICIPANT, ALIVE, NO
from edc_form_validators import FormValidator
from edc_visit_tracking.constants import LOST_VISIT, SCHEDULED
from edc_visit_tracking.form_validators import VisitFormValidator

from edc_action_item.site_action_items import site_action_items
from td_prn.action_items import MATERNALOFF_STUDY_ACTION

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

        self.validate_is_present()

        self.validate_last_alive_date()

    def validate_data_collection(self):
        if (self.cleaned_data.get('reason') == SCHEDULED
                and self.cleaned_data.get('study_status') == ON_STUDY
                and self.cleaned_data.get('require_crfs') == NO):
            msg = {'require_crfs': 'This field must be yes if participant'
                   'is on study and present.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_is_present(self):

        reason = self.cleaned_data.get('reason')

        if (reason == LOST_VISIT and
                self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant has been lost to follow up, '
                   'study status should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if self.cleaned_data.get('is_present') == YES:
            if self.cleaned_data.get('info_source') != PARTICIPANT:
                raise forms.ValidationError(
                    {'info_source': 'Source of information must be from '
                     'participant if participant is present.'})

    def validate_death(self):
        if (self.cleaned_data.get('survival_status') == DEAD
                and self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant is deceased, study status '
                   'should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        if self.cleaned_data.get('survival_status') != ALIVE:
            if (self.cleaned_data.get('is_present') == YES
                    or self.cleaned_data.get('info_source') == PARTICIPANT):
                msg = {'survival_status': 'Participant cannot be present or '
                       'source of information if their survival status is not'
                       'alive.'}
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

    def validate_reason_and_info_source(self):
        pass

    def validate_study_status(self):
        maternal_offstudy_cls = django_apps.get_model(
            'td_prn.maternaloffstudy')
        action_cls = site_action_items.get(
            maternal_offstudy_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item = action_item_model_cls.objects.get(
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
            if (action_item.parent_reference_model_obj
                and self.cleaned_data.get(
                    'report_datetime') >= action_item.parent_reference_model_obj.report_datetime):
                raise forms.ValidationError(
                    'Participant is scheduled to go offstudy.'
                    ' Cannot edit visit until offstudy form is completed.')
