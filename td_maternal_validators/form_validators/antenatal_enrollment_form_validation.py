from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from edc_form_validators import FormValidator


class AntenatalEnrollmentFormValidator(FormValidator):

    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def clean(self):
        self.validate_last_period_date(cleaned_data=self.cleaned_data)
        self.clean_rapid_test(cleaned_data=self.cleaned_data)

    def validate_last_period_date(self, cleaned_data=None):
        last_period_date = cleaned_data.get('last_period_date')
        report_datetime = cleaned_data.get('report_datetime')
        if last_period_date and (
                last_period_date > (report_datetime.date() - relativedelta(weeks=16))):
            message = {'last_period_date':
                       'LMP cannot be within 16weeks of report datetime. '
                       'Got LMP as {} and report datetime as {}'.format(last_period_date,
                                                                        report_datetime)
                       }
            self._errors.update(message)
            raise ValidationError(message)

        elif last_period_date and (
                last_period_date <= (report_datetime.date() - relativedelta(weeks=37))):
            message = {'last_period_date':
                       'LMP cannot be more than 36weeks of report datetime. '
                       'Got LMP as {} and report datetime as {}'.format(last_period_date,
                                                                        report_datetime)
                       }
            self._errors.update(message)
            raise ValidationError(message)

    def clean_rapid_test(self, cleaned_data=None):
        rapid_test_date = cleaned_data.get('rapid_test_date')
        subject_identifier = cleaned_data.get('subject_identifier')
        if rapid_test_date:
            try:
                antenatal_obj = self.antenatal_enrollment_cls.objects.get(
                    subject_identifier=subject_identifier)

                if rapid_test_date != antenatal_obj.rapid_test_date:
                    raise ValidationError(
                        'The rapid test result cannot be changed')
            except self.antenatal_enrollment_cls.DoesNotExist:
                pass
        return rapid_test_date

    # TDConsentVersionValidation
