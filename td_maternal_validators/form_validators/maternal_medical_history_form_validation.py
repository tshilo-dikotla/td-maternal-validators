from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator
from .maternal_form_validation_mixin import MaternalFormMixin


class MaternalMedicalHistoryFormValidator(FormValidator):

    rapid_test_result_model = 'td_maternal.rapidtestresult'
    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def rapid_testing_model_cls(self):
        return django_apps.get_model(self.rapid_test_result_model)

    @property
    def antenatal_enrollment_model_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def clean(self):
        status = MaternalFormMixin()
        condition = status.validate_hiv_result(cleaned_data=self.cleaned_data)
        self.validate_chronic_since_who_diagnosis_neg(
            cleaned_data=self.cleaned_data, condition=condition)
        self.validate_chronic_since_who_diagnosis_pos(
            cleaned_data=self.cleaned_data, condition=condition)
        self.validate_who_diagnosis_who_chronic_list(
            cleaned_data=self.cleaned_data, condition=condition)
        self.validate_mother_father_chronic_illness_multiple_selection()
        self.validate_mother_medications_multiple_selections()

    def validate_chronic_since_who_diagnosis_neg(self, cleaned_data=None, condition=False):
        if not condition and cleaned_data.get('chronic_since') == YES:
            if cleaned_data.get('who_diagnosis') != NOT_APPLICABLE:
                msg = {'who_diagnosis':
                       'The mother is HIV negative. Chronic_since should be NO '
                       'and Who Diagnosis should be Not Applicable'}
                self._errors.update(msg)
                raise ValidationError(msg)

            self.not_applicable_if(
                NO,
                field='chronic_since',
                field_applicable='who_diagnosis'
            )

    def validate_chronic_since_who_diagnosis_pos(self, cleaned_data=None, condition=False):
        if condition and cleaned_data.get('chronic_since') == NO:
            if cleaned_data.get('who_diagnosis') != NO:
                msg = {'who_diagnosis':
                       'The mother is HIV positive, because Chronic_since is '
                       'NO and Who Diagnosis should also be NO'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_who_diagnosis_who_chronic_list(self, cleaned_data=None, condition=False):
        self.m2m_required(
            m2m_field='who')

        if not condition and cleaned_data.get('who_diagnosis') == NOT_APPLICABLE:
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field='who')
        elif condition:
            if cleaned_data.get('who_diagnosis') == YES:
                qs = self.cleaned_data.get('who')
                if qs and qs.count() > 0:
                    selected = {obj.short_name: obj.name for obj in qs}
                if NOT_APPLICABLE in selected:
                    msg = {'who':
                           'Participant indicated that they had WHO stage III '
                           'and IV, list of diagnosis cannot be N/A'}
                    self._errors.update(msg)
                    raise ValidationError(msg)

    def validate_mother_father_chronic_illness_multiple_selection(self):
        m2m_fields = ('mother_chronic', 'father_chronic')
        for m2m_field in m2m_fields:
            self.m2m_required(
                m2m_field=m2m_field)

            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field=m2m_field)

    def validate_mother_medications_multiple_selections(self):
        self.m2m_required(
            m2m_field='mother_medications')
        self.m2m_single_selection_if(
            NOT_APPLICABLE,
            m2m_field='mother_medications')

    def validate_positive_mother_seropositive_yes(self, cleaned_data=None, condition=False):
        if condition:
            self.required_if(
                YES,
                field='sero_posetive',
                field_required='date_hiv_diagnosis')
            fields_applicable = ('perinataly_infected', 'know_hiv_status',
                                 'lowest_cd4_known')
            for field_applicable in fields_applicable:
                self.applicable_if(
                    YES,
                    field='sero_posetive',
                    field_applicable=field_applicable)

            if cleaned_data.get('sero_posetive') == YES:
                required_fields = ('cd4_count', 'cd4_date',
                                   'is_date_estimated')
                for required in required_fields:
                    self.required_if(
                        YES,
                        field='lowest_cd4_known',
                        field_required=required)
            if cleaned_data.get('sero_posetive') == NO:
                msg = {'sero_posetive':
                       'The mother is HIV Positive, The field for whether she is sero'
                       'positive should not be NO'}
                raise ValidationError(msg)

    def validate_negative_mother_seropositive_no(self, cleaned_data=None, condition=False):
        if not condition:
            if cleaned_data.get('sero_posetive') == YES:
                msg = {'sero_posetive':
                       'The Mother is HIV Negative she cannot be Sero Positive'}
                self._errors.update(msg)
                raise ValidationError(msg)
