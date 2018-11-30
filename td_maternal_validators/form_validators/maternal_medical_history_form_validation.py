from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, POS, NEG, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator


class MaternalMedicalHistoryFormValidator(FormValidator):

    rapid_test_result_model = 'td_maternal.rapidtestresult'
    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def rapid_testing_model_cls(self):
        return django_apps.get_model(self.rapid_test_result_model)

    @property
    def antenatal_enrollment_model_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)\


    def clean(self):
        self.required_if(
            YES,
            field='chronic_since',
            field_required='who_diagnosis'
        )
        self.validate_hiv_result(cleaned_data=self.cleaned_data)

    def validate_hiv_result(self, cleaned_data=None):
        rapid_test_result = self.rapid_testing_model_cls.objects.filter().\
            order_by('created').last()
        if rapid_test_result:
            condition = rapid_test_result.result == NEG

        else:
            raise ValidationError('rapid testing results does not exist.')
            try:
                antenatal_enrollment = self.antenatal_enrollment_model_cls.objects.get(
                    subject_identifier=cleaned_data.get('subject_identifier'))

                condition = (antenatal_enrollment.enrollment_hiv_status == POS or
                             antenatal_enrollment.week32_result == POS or
                             antenatal_enrollment.rapid_test_result == POS)

                self.validate_chronic_since_who_diagnosis_neg(condition)

            except self.antenatal_enrollment_model_cls.DoesNotExist:
                raise ValidationError('Fill out Antenatal Enrollment Form.')

    def validate_chronic_since_who_diagnosis_neg(self):

        if('chronic_since') == YES:
            if (('who_diagnosis') == NO or
                ('who_diagnosis') == YES or
                    ('who_diagnosis') == NOT_APPLICABLE):
                msg = {'The mother is HIV negative. Chronic_since should be NO'
                       'and Who Diagnosis should be Not Applicable'}
                self._errors.update(msg)
                raise ValidationError(msg)
            else:
                if ('chronic_since') == NO:
                    if ('who_diagnosis') != NOT_APPLICABLE:
                        msg = {
                            'The mother is HIV negative.'
                            'Who Diagnosis should be Not Applicable'}

        self._errors.update(msg)
        raise ValidationError(msg)

    def validate_chronic_since_who_diagnosis_pos(self):

        if ('chronic_since') == NO:
            if ('who_diagnosis') != NO:
                msg = {'The mother is HIV positive, because Chronic_since is NO'
                       'and Who Diagnosis should also be NO'}
        self._errors.update(msg)
        raise ValidationError(msg)

    def validate_who_diagnosis_who_chronic_list(self):

        if not ('who'):
            msg = {'Question5: Mother has prior chronic illness, they should be listed'}

        if ('who_diagnosis') == NOT_APPLICABLE:
            if self.validate_not_applicable_not_there('who'):
                msg = {
                    'Question5: Participant is HIV Negative,'
                    'do not give a listing, rather give N/A'}

            if self.validate_not_applicable_and_other_options('who'):
                msg = {'Question5: Participant is HIV Negative,'
                       'do not give a listing, only give N/A'}

        if ('who_diagnosis') == YES:
            if self.validate_not_applicable_in_there('who'):
                msg = {'Question5: Participant indicated that they had'
                       'WHO stage III and IV, list of diagnosis cannot be N/A'}

        if ('who_diagnosis') == NO:
            if self.validate_not_applicable_not_there('who'):
                msg = {'Question5: The mother does not have prior who'
                       'stage III and IV illnesses. Should provide N/A'}

            if self.validate_not_applicable_and_other_options('who'):
                msg = {'Question5: The mother does not have prior who'
                       'stage III and IV illnesses. Should only provide N/A'}
        self._errors.update(msg)
        raise ValidationError(msg)

    def validate_mother_medications_multiple_selections(self):

        if self.validate_many_to_many_not_blank('mother_medications'):
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
