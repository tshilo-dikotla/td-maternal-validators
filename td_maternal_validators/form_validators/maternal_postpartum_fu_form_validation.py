from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, POS
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
        required_fields = {'hospitalized': 'hospitalization_reason',
                           'new_diagnoses': 'diagnoses'}
        for field, required_field in required_fields.items():
            self.m2m_required_if(
                response=YES,
                field=field,
                m2m_field=required_field)

        self.required_if(
            YES,
            field='hospitalized',
            field_required='hospitalization_days')

        self.validate_hiv_result(cleaned_data=self.cleaned_data)

    def validate_hiv_result(self, cleaned_data=None):
        rapid_test_result = self.rapid_testing_model_cls.objects.filter().\
            order_by('created').last()
        if rapid_test_result:
            condition = rapid_test_result.result == POS

            self.validate_who_diagnoses(condition)

        else:
            raise ValidationError('rapid testing results does not exist.')
            try:
                antenatal_enrollment = self.antenatal_enrollment_model_cls.objects.get(
                    subject_identifier=cleaned_data.get('subject_identifier'))

                condition = (antenatal_enrollment.enrollment_hiv_status == POS or
                             antenatal_enrollment.week32_result == POS or
                             antenatal_enrollment.rapid_test_result == POS)

                self.validate_who_diagnoses(condition)

            except self.antenatal_enrollment_model_cls.DoesNotExist:
                raise ValidationError('Fill out Antenatal Enrollment Form.')

    def validate_who_diagnoses(self, condition=None):
        self.applicable_if_true(
            condition=condition,
            field_applicable='has_who_dx',
            applicable_msg='The mother is positive, question 10 for WHO '
                           'Stage III/IV should not be N/A',
            not_applicable_msg='The mother is Negative, question 10 for '
                               'WHO Stage III/IV should be N/A'
        )
        if condition:
            self.m2m_required_if(
                YES,
                field='has_who_dx',
                m2m_field='who'
            )
