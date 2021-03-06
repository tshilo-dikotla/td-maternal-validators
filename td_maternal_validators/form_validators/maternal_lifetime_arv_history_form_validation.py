from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, RESTARTED, CONTINUOUS, STOPPED, OTHER, \
    NOT_APPLICABLE
from edc_form_validators import FormValidator

from td_maternal.helper_classes import MaternalStatusHelper
from .crf_form_validator import TDCRFFormValidator
from .form_validator_mixin import TDFormValidatorMixin


class MaternalLifetimeArvHistoryFormValidator(TDCRFFormValidator,
                                              TDFormValidatorMixin,
                                              FormValidator):
    maternal_consent_model = 'td_maternal.subjectconsent'
    ob_history_model = 'td_maternal.maternalobstericalhistory'
    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'
    medical_history_model = 'td_maternal.maternalmedicalhistory'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    @property
    def maternal_consent_model_cls(self):
        return django_apps.get_model(self.maternal_consent_model)

    @property
    def maternal_medical_history_model_cls(self):
        return django_apps.get_model(self.medical_history_model)

    @property
    def maternal_ob_history_model_cls(self):
        return django_apps.get_model(self.ob_history_model)

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.validate_prior_preg(cleaned_data=self.cleaned_data)

        self.validate_maternal_consent(cleaned_data=self.cleaned_data)

        self.validate_prev_preg(cleaned_data=self.cleaned_data)
        self.validate_hiv_test_date_antenatal_enrollment()
        self.validate_other_mother()

    def validate_prior_preg(self, cleaned_data=None):
        responses = (CONTINUOUS, RESTARTED)
        if (cleaned_data.get('preg_on_haart') == NO
                and self.cleaned_data.get('prior_preg') in responses):
            msg = {'prior_preg': 'You indicated that the mother was NOT on'
                   ' triple ARV when she got pregnant. Please correct.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if (cleaned_data.get('preg_on_haart') == YES
                and self.cleaned_data.get('prior_preg') in [STOPPED, NOT_APPLICABLE]):
            msg = {'prior_preg': 'You indicated that the mother was still on '
                                 'triple ARV when she got pregnant, this field'
                                 ' s required.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        qs = self.cleaned_data.get('prior_arv')
        if qs and qs.count() >= 1:
            selected = {obj.short_name: obj.name for obj in qs}
            if (self.cleaned_data.get('prior_preg') != NOT_APPLICABLE and
                    NOT_APPLICABLE in selected):
                message = {
                    'prior_arv':
                    'This field is applicable.'}
                self._errors.update(message)
                raise ValidationError(message)
            elif (self.cleaned_data.get('prior_preg') == NOT_APPLICABLE and
                    NOT_APPLICABLE not in selected):
                message = {
                    'prior_arv':
                    'This field is not applicable.'}

    def validate_other_mother(self):
        selections = [NOT_APPLICABLE]
        self.m2m_single_selection_if(
            *selections,
            m2m_field='prior_arv')
        self.m2m_other_specify(
            OTHER,
            m2m_field='prior_arv',
            field_other='prior_arv_other')

    def validate_maternal_consent(self, cleaned_data=None):
        if cleaned_data.get('haart_start_date'):
            id = None
            if self.instance:
                id = self.instance.id
            try:
                maternal_consent = self.validate_against_consent(id=id)
                if cleaned_data.get('report_datetime') < maternal_consent.consent_datetime:
                    msg = {'report_datetime': 'Report datetime CANNOT be '
                                              'before consent datetime'}
                    self._errors.update(msg)
                    raise ValidationError(msg)

                if cleaned_data.get('haart_start_date') < maternal_consent.dob:
                    msg = {'haart_start_date': 'Date of triple ARVs first '
                                               'started CANNOT be before DOB.'}
                    self._errors.update(msg)
                    raise ValidationError(msg)
            except self.maternal_consent_model_cls.DoesNotExist:
                raise ValidationError('Maternal Consent does not exist.')

    def validate_prev_preg(self, cleaned_data=None):
        ob_history = self.maternal_ob_history_model_cls.objects.filter(
            maternal_visit__subject_identifier=cleaned_data.get(
                'maternal_visit').subject_identifier)
        if not ob_history:
            raise ValidationError(
                'Please fill in the Maternal Obsterical History form first.')
        else:
            condition = ob_history[0].prev_pregnancies > 1
            fields_applicable = ['prev_preg_azt',
                                 'prev_sdnvp_labour', 'prev_preg_haart']
            for field_applicable in fields_applicable:
                self.applicable_if_true(condition,
                                        field_applicable=field_applicable)

    def validate_hiv_test_date_antenatal_enrollment(self):
        try:
            medical_history = self.maternal_medical_history_model_cls.objects.get(
                maternal_visit__subject_identifier=self.cleaned_data.get('maternal_visit').subject_identifier)
        except self.maternal_medical_history_model_cls.DoesNotExist:
            raise forms.ValidationError(
                'Date of diagnosis required, complete Maternal Medical '
                'History form before proceeding.')
        else:
            if(self.cleaned_data.get('haart_start_date') and
               self.cleaned_data.get('haart_start_date') < medical_history.date_hiv_diagnosis):
                msg = {'haart_start_date':
                       'Haart start date cannot be before HIV diagnosis date.'}
                self._errors.update(msg)

        try:
            antenatal_enrollment = self.antenatal_enrollment_cls.objects.get(
                subject_identifier=self.cleaned_data.get(
                    'maternal_visit').subject_identifier)
        except self.antenatal_enrollment_cls.DoesNotExist:
            raise forms.ValidationError(
                'Date of HIV test required, complete Antenatal Enrollment'
                ' form before proceeding.')
        else:
            if(self.cleaned_data.get('haart_start_date') and
                    self.cleaned_data.get('haart_start_date') < antenatal_enrollment.week32_test_date):
                msg = {'haart_start_date':
                       'Haart start date cannot be before date of HIV test.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    @property
    def subject_screening(self):
        try:
            return self.subject_screening_cls.objects.get(
                subject_identifier=self.cleaned_data.get(
                    'maternal_visit').appointment.subject_identifier)
        except self.subject_screening_cls.DoesNotExist:
            return None
