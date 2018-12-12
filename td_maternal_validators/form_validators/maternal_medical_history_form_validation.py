# from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator
from .maternal_form_validation_mixin import MaternalFormMixin
# from django.views.decorators.http import condition
# from builtins import None


class MaternalMedicalHistoryFormValidator(MaternalFormMixin, FormValidator):

    rapid_test_result_model = 'td_maternal.rapidtestresult'
    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def rapid_testing_model_cls(self):
        return django_apps.get_model(self.rapid_test_result_model)

    @property
    def antenatal_enrollment_model_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def clean(self):
        self.required_if(
            YES,
            field='chronic_since',
            field_required='who_diagnosis',
            inverse=False
        )
        self.validate_chronic_since_who_diagnosis_pos(
            cleaned_data=self.cleaned_data)
        self.validate_chronic_since_who_diagnosis_neg(
            cleaned_data=self.cleaned_data)
        self.validate_who_diagnosis_who_chronic_list(
            cleaned_data=self.cleaned_data)

    def validate_chronic_since_who_diagnosis_neg(self, cleaned_data=None):

        if cleaned_data.get('chronic_since') == YES:
            if (('who_diagnosis') == {NO, YES, NOT_APPLICABLE}):
                msg = {'chronic_since': 'The mother is HIV negative.'
                       'Chronic_since should be NO'
                       'and Who Diagnosis should be Not Applicable'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_chronic_since_who_diagnosis_pos(self, cleaned_data=None):

        if cleaned_data.get('chronic_since') == NO:
            if self.cleaned_data.get('who_diagnosis') != NO or NOT_APPLICABLE:
                msg = {"chronic_since": 'The mother is HIV positive, because'
                       'chronic_since is NO and Who Diagnosis should also be NO'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_who_diagnosis_who_chronic_list(self, cleaned_data=None):

        if not cleaned_data.get('who'):
            msg = {'Question5: Mother has prior chronic illness, they should be listed'}

        if self.cleaned_data.get('who_diagnosis') == NOT_APPLICABLE or (
                self.cleaned_data.get('who_diagnosis') == NO):
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field='who')

        if self.cleaned_data.get('who_diagnosis') == YES:
            qs = self.cleaned_data.get('who')
            if qs and qs.count() > 1:
                selected = {obj.short_name: obj.name for obj in qs}
                for selection in selected:
                    if NOT_APPLICABLE in selection:
                        msg = {'who': 'Question5: Participant indicated that they had'
                               'WHO stage III and IV, list of diagnosis cannot be N/A'}

                        self._errors.update(msg)
                        raise ValidationError(msg)

    def validate_mother_medications_multiple_selections(self, cleaned_data=None):

        if cleaned_data.get('mother_medications'):
            msg = {'Question10: The field for the mothers'
                   'medications should not be left blank'}

        if self.validate_not_applicable_and_other_options('mother_medications'):
            msg = {'Question10: You cannot select options that have N/A in them'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_positive_mother_seropositive_yes(self):
        required_fields = ['perinataly_infected', 'know_hiv_status',
                           'lowest_cd4_known']
        for required in required_fields:
            if required in self.cleaned_data:
                self.required_if(
                    YES,
                    field='sero_posetive',
                    field_required=required
                )

    def validate_negative_mother_seropositive_no_cd4_not(self):
        required_fields = ['lowest_cd4_known', 'cd4_count',
                           'cd4_date', 'is_date_estimated']
        for required in required_fields:
            if required in self.cleaned_data:
                self.required_if(
                    YES,
                    field='sero_posetive',
                    field_required=required
                )

    def validate_haart_start_date(self, cleaned_data=None):
        if cleaned_data.get('haart_start_date'):
            if cleaned_data('haart_start_date') < cleaned_data.get('date_hiv_diagnosis'):
                msg = {'Haart start date cannot be before HIV diagnosis date.'}
                self._errors.update(msg)
                raise ValidationError(msg)
