from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, NEG
from dateutil.relativedelta import relativedelta
from ..form_validators import AntenatalEnrollmentFormValidator
from .models import AntenatalEnrollment


class TestAntenatalEnrollmentForm(TestCase):

    def setUp(self):
        self.subject_identifier = '1234ABC'
        self.antenatal_enrollment = AntenatalEnrollment.objects.create(
            subject_identifier=self.subject_identifier,
            enrollment_hiv_status=NEG, week32_result=POS,
            rapid_test_result=POS, rapid_test_date=get_utcnow().date())
        self.antenatal_enrollment_model = 'td_maternal_validators.antenatalenrollment'
        AntenatalEnrollmentFormValidator.antenatal_enrollment_model =\
            self.antenatal_enrollment_model

    def test_LMP_within_16wks_of_report_datetime_invalid(self):
        '''Asserts if an exception is raised if last period date is within
        16 weeks of the report datetime.'''

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'last_period_date': get_utcnow().date() - relativedelta(weeks=2)
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('last_period_date', form_validator._errors)

    def test_LMP_16wksormore_than_report_datetime_valid(self):
        '''Tests if last period date > 16 weeks before report date time validates
        or fails the tests if Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'last_period_date': get_utcnow().date() - relativedelta(weeks=16)
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_LMP_more_than_36wks_of_report_datetime_invalid(self):
        '''Asserts if an exception is raised if last period date is more than
        36 weeks of the report datetime.'''

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'last_period_date': get_utcnow().date() - relativedelta(weeks=37)
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('last_period_date', form_validator._errors)

    def test_LMP_between_16wks_36wks_of_reportdatetime_valid(self):
        '''Tests if last period date is <= 36 weeks & > 16 weeks of report
        datetime validates or fails the tests if Validation Error is
        raised unexpectedly.'''

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'last_period_date': get_utcnow().date() - relativedelta(weeks=20)
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_rapid_test_date_changed_invalid(self):
        '''Asserts if an exception is raised if the rapid test date does not
        match that of the antenatal enrollment object.'''

        cleaned_data = {
            'rapid_test_date': get_utcnow().date() - relativedelta(days=5),
            'subject_identifier': self.subject_identifier
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_rapid_test_date_valid(self):
        '''Tests if last period date > 16 weeks before report date time validates
        or fails the tests if Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'rapid_test_date': get_utcnow().date(),
            'subject_identifier': self.subject_identifier
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_antenatal_object_does_not_exist(self):
        '''Tests if antenatal object does not exist cleaned data validates
        or fails the tests if Validation Error is raised unexpectedly.'''

        self.antenatal_enrollment.delete()
        cleaned_data = {
            'rapid_test_date': get_utcnow().date() - relativedelta(days=3),
            'subject_identifier': self.subject_identifier}
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')