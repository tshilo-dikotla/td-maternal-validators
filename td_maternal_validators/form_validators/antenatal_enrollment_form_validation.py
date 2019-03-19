from dateutil.relativedelta import relativedelta
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator

from td_maternal.helper_classes import EnrollmentHelper

from .form_validator_mixin import TDFormValidatorMixin


class AntenatalEnrollmentFormValidator(TDFormValidatorMixin, FormValidator):

    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def clean(self):
        self.required_if(
            YES,
            field='knows_lmp',
            field_required='last_period_date'
        )
        self.validate_last_period_date(cleaned_data=self.cleaned_data)
        self.clean_rapid_test(cleaned_data=self.cleaned_data)
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))

        enrollment_helper = EnrollmentHelper(
            instance_antenatal=self.antenatal_enrollment_cls(
                **self.cleaned_data),
            exception_cls=forms.ValidationError)
        enrollment_helper.raise_validation_error_for_rapidtest()

    def validate_last_period_date(self, cleaned_data=None):
        last_period_date = cleaned_data.get('last_period_date')
        report_datetime = cleaned_data.get('report_datetime')
        if last_period_date and (
                last_period_date > (
                    report_datetime.date() - relativedelta(weeks=16))):
            message = {'last_period_date':
                       'LMP cannot be within 16weeks of report datetime. '
                       f'Got LMP as {last_period_date} and report datetime as '
                       f'{report_datetime}'}
            self._errors.update(message)
            raise ValidationError(message)

        elif last_period_date and (
                last_period_date <= (
                    report_datetime.date() - relativedelta(weeks=37))):
            message = {'last_period_date':
                       'LMP cannot be more than 36weeks of report datetime. '
                       f'Got LMP as {last_period_date} and report datetime as '
                       f'{report_datetime}'}
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
