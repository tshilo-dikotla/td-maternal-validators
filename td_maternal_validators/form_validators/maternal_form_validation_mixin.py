from edc_constants.constants import NEG, POS
from django.core.exceptions import ValidationError


class MaternalFormMixin:

    def validate_hiv_result(self, cleaned_data=None):

        condition = None

        rapid_test_result = self.rapid_testing_model_cls.objects.filter().\
            order_by('created').last()

        if rapid_test_result:
            condition = rapid_test_result.result == NEG
        else:
            try:
                antenatal_enrollment = self.antenatal_enrollment_model_cls.objects.get(
                    registered_subject=cleaned_data.get('registered_subject'))

            except self.antenatal_enrollment_model_cls.DoesNotExist:
                raise ValidationError('Fill out Antenatal Enrollment Form.')
            else:
                condition = (antenatal_enrollment.enrollment_hiv_status == POS or
                             antenatal_enrollment.week32_result == POS or
                             antenatal_enrollment.rapid_test_result == POS)
        return condition
