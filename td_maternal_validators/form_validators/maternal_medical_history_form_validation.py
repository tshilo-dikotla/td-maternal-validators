from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, NOT_APPLICABLE, NEG, POS, OTHER
from edc_form_validators import FormValidator
from td_maternal.helper_classes import MaternalStatusHelper


class MaternalMedicalHistoryFormValidator(FormValidator):

    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    @property
    def maternal_visit_cls(self):
        return django_apps.get_model(self.maternal_visit_model)

    def clean(self):
        self.validate_chronic_since_who_diagnosis_neg(
            cleaned_data=self.cleaned_data)
        self.validate_chronic_since_who_diagnosis_pos(
            cleaned_data=self.cleaned_data)
        self.validate_who_diagnosis_who_chronic_list(
            cleaned_data=self.cleaned_data)
        self.validate_mother_father_chronic_illness_multiple_selection()
        self.validate_mother_medications_multiple_selections()
        self.validate_positive_mother_seropositive_yes(
            cleaned_data=self.cleaned_data)
        self.validate_negative_mother_seropositive_no(
            cleaned_data=self.cleaned_data)
        self.validate_negative_mother_seropositive_no_cd4_not(
            cleaned_data=self.cleaned_data)
        self.validate_hiv_diagnosis_date(cleaned_data=self.cleaned_data)
        self.validate_other_mother()
        self.validate_other_father()
        self.validate_other_mother_medications()

    def validate_chronic_since_who_diagnosis_neg(self, cleaned_data=None):
        #                 print(self.maternal_status_helper.hiv_status)
        if self.maternal_status_helper.hiv_status == NEG:
            if cleaned_data.get('chronic_since') == YES:
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

    def validate_chronic_since_who_diagnosis_pos(self, cleaned_data=None):
        status_helper = MaternalStatusHelper(
            cleaned_data.get('maternal_visit'))
        subject_status = status_helper.hiv_status

        if cleaned_data.get('chronic_since') == NO and subject_status == POS:
            if cleaned_data.get('who_diagnosis') != NO:
                msg = {'who_diagnosis':
                       'The mother is HIV positive, because Chronic_since is '
                       'NO and Who Diagnosis should also be NO'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_who_diagnosis_who_chronic_list(self, cleaned_data=None):
        self.m2m_required(
            m2m_field='who')
        status_helper = MaternalStatusHelper(
            cleaned_data.get('maternal_visit'))
        subject_status = status_helper.hiv_status

        if subject_status == NEG and cleaned_data.get('who_diagnosis') == NOT_APPLICABLE:
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field='who')

        if subject_status == POS and cleaned_data.get('who_diagnosis') == YES:
            qs = self.cleaned_data.get('who')
            if qs and qs.count() > 0:
                selected = {obj.short_name: obj.name for obj in qs}
            if NOT_APPLICABLE in selected:
                msg = {'who':
                       'Participant indicated that they had WHO stage III '
                       'and IV, list of diagnosis cannot be N/A'}
                self._errors.update(msg)
                raise ValidationError(msg)

        if subject_status == POS and cleaned_data.get('who_diagnosis') == NO:
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field='who')

    def validate_mother_father_chronic_illness_multiple_selection(self):
        m2m_fields = ('mother_chronic', 'father_chronic')
        for m2m_field in m2m_fields:
            self.m2m_required(
                m2m_field=m2m_field)

            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field=m2m_field)

    def validate_other_mother(self):
        selections = [OTHER, NOT_APPLICABLE]
        self.m2m_single_selection_if(
            *selections,
            m2m_field='mother_chronic')
        self.m2m_other_specify(
            OTHER,
            m2m_field='mother_chronic',
            field_other='mother_chronic_other')

    def validate_other_father(self):
        selections = [OTHER, NOT_APPLICABLE]
        self.m2m_single_selection_if(
            *selections,
            m2m_field='father_chronic')
        self.m2m_other_specify(
            OTHER,
            m2m_field='father_chronic',
            field_other='father_chronic_other')

    def validate_mother_medications_multiple_selections(self):
        self.m2m_required(
            m2m_field='mother_medications')

    def validate_other_mother_medications(self):
        selections = [OTHER, NOT_APPLICABLE]
        self.m2m_single_selection_if(
            *selections,
            m2m_field='mother_medications')
        self.m2m_other_specify(
            OTHER,
            m2m_field='mother_medications',
            field_other='mother_medications_other')

    def validate_positive_mother_seropositive_yes(self, cleaned_data=None):
        status_helper = MaternalStatusHelper(
            cleaned_data.get('maternal_visit'))
        subject_status = status_helper.hiv_status

        if subject_status == POS:
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
                       ' positive should not be NO'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_negative_mother_seropositive_no(self, cleaned_data=None):
        if self.maternal_status_helper.hiv_status == NEG:
            if cleaned_data.get('sero_posetive') == YES:
                msg = {'sero_posetive':
                       'The Mother is HIV Negative she cannot be Sero Positive'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if cleaned_data.get('date_hiv_diagnosis'):
                msg = {'date_hiv_diagnosis':
                       'The Mother is HIV Negative, the approximate date of'
                       ' diagnosis should not be supplied'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if cleaned_data.get('perinataly_infected') != NOT_APPLICABLE:
                msg = {'perinataly_infected':
                       'The Mother is HIV Negative, the field for whether '
                       'she was Perinataly Infected should be N/A'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if cleaned_data.get('know_hiv_status') != NOT_APPLICABLE:
                msg = {'know_hiv_status':
                       'The Mother is HIV Negative, the field for whether '
                       'anyone knows the if the mother is HIV Positive should be N/A'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_negative_mother_seropositive_no_cd4_not(self, cleaned_data=None):
        status_helper = MaternalStatusHelper(
            cleaned_data.get('maternal_visit'))
        subject_status = status_helper.hiv_status

        condition = subject_status == POS

        self.applicable_if_true(
            condition,
            field_applicable='lowest_cd4_known',
            not_applicable_msg=(
                'The Mother is HIV Negative, the field for whether '
                'the lowest CD4 count is known should be N/A')
        )

        required_fields = ('cd4_count', 'cd4_date', 'is_date_estimated')
        for required in required_fields:
            self.required_if_true(
                condition,
                field_required=required,
                not_required_msg=(
                    f'The Mother is HIV Negative, the field for {required} '
                    'should be left blank')
            )

    def validate_hiv_diagnosis_date(self, cleaned_data=None):

        if cleaned_data.get('sero_posetive') == YES:
            antenatal_enrollment = self.antenatal_enrollment_cls.objects.get(
                subject_identifier=cleaned_data.get('maternal_visit').appointment.subject_identifier)
            if antenatal_enrollment.week32_test_date != cleaned_data.get('date_hiv_diagnosis'):
                msg = {'date_hiv_diagnosis':
                       'HIV diagnosis date should match date '
                       f'{antenatal_enrollment.week32_test_date} at Antenatal '
                       'Enrollment'}
                self._errors.update(msg)
                raise ValidationError(msg)

    @property
    def maternal_status_helper(self):
        cleaned_data = self.cleaned_data
        status_helper = MaternalStatusHelper(
            cleaned_data.get('maternal_visit'))
        return status_helper
