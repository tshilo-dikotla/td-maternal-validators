from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator


class RapidTestResultFormValidator(FormValidator):

    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def clean(self):

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='result_date',
            required_msg=('If a rapid test was processed, what is '
                          f'the result date of the rapid test?'),
            not_required_msg=('If a rapid test was not processed, '
                              f'please do not provide the result date.'),
            inverse=True)

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='result',
            required_msg=('If a rapid test was processed, what is '
                          f'the result of the rapid test?'),
            not_required_msg=('If a rapid test was not processed, '
                              f'please do not provide the result.'),
            inverse=True)
        self.validate_enrolment_rapid_test_date()

    def validate_enrolment_rapid_test_date(self):
        try:
            antenatal_enrollment = self.antenatal_enrollment_cls.objects.get(
                subject_identifier=self.cleaned_data.get('maternal_visit').appointment.subject_identifier)
        except self.antenatal_enrollment_cls.DoesNotExist:
            message = {'rapid_test_done':
                       'Antenatal enrollment not found, please complete enrollment form.'}
            self._errors.update(message)
            raise ValidationError(message)
        else:
            if antenatal_enrollment.rapid_test_date:
                if self.cleaned_data.get('result_date') < antenatal_enrollment.rapid_test_date:
                    message = {
                        'result_date':
                        'Rapid test date cannot be before enrollment rapid test date.'}
                    self._errors.update(message)
                    raise ValidationError(message)
