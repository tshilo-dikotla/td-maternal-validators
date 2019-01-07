from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, POS, NOT_APPLICABLE, NO
from edc_form_validators import FormValidator


class MaternalPostPartumFuFormValidator(FormValidator):

    rapid_test_result_model = 'td_maternal.rapidtestresult'
    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def rapid_testing_model_cls(self):
        return django_apps.get_model(self.rapid_test_result_model)

    @property
    def antenatal_enrollment_model_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def clean(self):
        required_fields = ('hospitalization_reason', 'diagnoses')
        for required_field in required_fields:
            self.m2m_required(
                m2m_field=required_field
            )

        if self.cleaned_data.get('new_diagnoses') == NO:
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field='diagnoses'
            )

        if self.cleaned_data.get('new_diagnoses') == YES:
            qs = self.cleaned_data.get('diagnoses').values_list(
                'short_name', flat=True)
            selection = list(qs.all())
            if NOT_APPLICABLE in selection:
                msg = {'diagnoses':
                       'Question4: Participant has new diagnoses, '
                       'list of diagnosis cannot be N/A'}
                self._errors.update(msg)
                raise ValidationError(msg)

        if self.cleaned_data.get('hospitalized') == YES:
            qs = self.cleaned_data.get('hospitalization_reason').values_list(
                'short_name', flat=True)
            selection = list(qs.all())
            if NOT_APPLICABLE in selection:
                msg = {'hospitalization_reason':
                       'Question7: Participant was hospitalized, reasons cannot be N/A'}
                self._errors.update(msg)
                raise ValidationError(msg)

        self.required_if(
            YES,
            field='hospitalized',
            field_required='hospitalization_days')

        if self.cleaned_data.get('hospitalized') == NO:
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field='hospitalization_reason')

        self.validate_hiv_result(cleaned_data=self.cleaned_data)

    def validate_hiv_result(self, cleaned_data=None):
        rapid_test_result = self.rapid_testing_model_cls.objects.filter().\
            order_by('created').last()
        if rapid_test_result:
            condition = rapid_test_result.result == POS

            self.validate_who_diagnoses(cleaned_data, condition)

        else:
            raise ValidationError('rapid testing results does not exist.')
            try:
                antenatal_enrollment = self.antenatal_enrollment_model_cls.objects.get(
                    subject_identifier=cleaned_data.get('subject_identifier'))

                condition = (antenatal_enrollment.enrollment_hiv_status == POS or
                             antenatal_enrollment.week32_result == POS or
                             antenatal_enrollment.rapid_test_result == POS)

                self.validate_who_diagnoses(cleaned_data, condition)

            except self.antenatal_enrollment_model_cls.DoesNotExist:
                raise ValidationError('Fill out Antenatal Enrollment Form.')

    def validate_who_diagnoses(self, cleaned_data=None, condition=None):
        self.applicable_if_true(
            condition=condition,
            field_applicable='has_who_dx',
            applicable_msg='The mother is positive, question 10 for WHO '
                           'Stage III/IV should not be N/A',
            not_applicable_msg='The mother is Negative, question 10 for '
                               'WHO Stage III/IV should be N/A'
        )
        self.m2m_required(m2m_field='who')
        if not condition:
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field='who')
        if condition:
            if cleaned_data.get('has_who_dx') == YES:
                qs = self.cleaned_data.get('who').values_list(
                    'short_name', flat=True)
                selection = list(qs.all())
                if NOT_APPLICABLE in selection:
                    msg = {'who':
                           'Question 10 is indicated as YES, who listing cannot be N/A'}
                    self._errors.update(msg)
                    raise ValidationError(msg)
            else:
                self.m2m_single_selection_if(
                    NOT_APPLICABLE,
                    m2m_field='who')
