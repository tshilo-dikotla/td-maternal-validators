from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, NEG, YES, NO

from ..form_validators import AntenatalEnrollmentFormValidator
from .models import (AntenatalEnrollment, SubjectScreening,
                     SubjectConsent, TdConsentVersion)


@tag('ae')
class TestAntenatalEnrollmentForm(TestCase):

    def setUp(self):
        AntenatalEnrollmentFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        AntenatalEnrollmentFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        AntenatalEnrollmentFormValidator.subject_screening_model = \
            'td_maternal_validators.subjectscreening'

        self.subject_identifier = '11111111'

        self.subject_screening = SubjectScreening.objects.create(
            subject_identifier='11111111',
            screening_identifier='ABC12345',
            age_in_years=22)

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')

        self.td_consent_version = TdConsentVersion.objects.create(
            screening_identifier=self.subject_screening.screening_identifier,
            version='3', report_datetime=get_utcnow())

    def test_LMP_within_16wks_of_report_datetime_invalid(self):
        '''Asserts if an exception is raised if last period date is within
        16 weeks of the report datetime.'''

        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'report_datetime': get_utcnow(),
            'last_period_date': get_utcnow().date() - relativedelta(weeks=2),
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
            'rapid_test_date': get_utcnow().date()
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('last_period_date', form_validator._errors)

    def test_LMP_16wksormore_than_report_datetime_valid(self):
        '''Tests if last period date > 16 weeks before report date time validates
        or fails the tests if Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'report_datetime': get_utcnow(),
            'last_period_date': get_utcnow().date() - relativedelta(weeks=16),
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
            'week32_test_date': get_utcnow().date(),
            'rapid_test_date': get_utcnow().date()
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
            'subject_identifier': self.subject_identifier,
            'report_datetime': get_utcnow(),
            'last_period_date': get_utcnow().date() - relativedelta(weeks=37),
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
            'rapid_test_date': get_utcnow().date()
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
            'subject_identifier': self.subject_identifier,
            'report_datetime': get_utcnow(),
            'last_period_date': get_utcnow().date() - relativedelta(weeks=20),
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
            'rapid_test_date': get_utcnow().date(),
            'week32_test_date': get_utcnow().date()
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
        self.antenatal_enrollment = AntenatalEnrollment.objects.create(
            subject_identifier='1234ABC',
            enrollment_hiv_status=NEG, week32_result=POS,
            rapid_test_result=POS, rapid_test_date=get_utcnow().date())

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_date': get_utcnow().date() - relativedelta(days=5),
            'week32_test_date': get_utcnow().date() - relativedelta(days=5)
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_rapid_test_date_valid(self):
        '''Tests if last period date > 16 weeks before report date time validates
        or fails the tests if Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_done': YES,
            'rapid_test_date': get_utcnow().date(),
            'rapid_test_result': NEG,
            'week32_test_date': get_utcnow().date()
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

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_date': get_utcnow().date() - relativedelta(days=3),
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
            'week32_test_date': get_utcnow().date() - relativedelta(days=3)}
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_current_hiv_status_invalid_1(self):
        '''Tests if last period date > 16 weeks before report date time validates
        or fails the tests if Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_done': NO,
            'week32_test': YES,
            'current_hiv_status': NEG,
            'week32_result': POS
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('current_hiv_status', form_validator._errors)

    def test_current_hiv_status_invalid_2(self):
        '''Tests if last period date > 16 weeks before report date time validates
        or fails the tests if Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_done': NO,
            'week32_test': NO,
            'current_hiv_status': NEG,
            'week32_result': None
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('current_hiv_status', form_validator._errors)

    def test_rapid_test_date_invalid(self):
        '''Tests if last period date > 16 weeks before report date time validates
        or fails the tests if Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_done': YES,
            'rapid_test_date': None,
            'rapid_test_result': NEG
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('rapid_test_date', form_validator._errors)

    def test_rapid_test_result_invalid(self):
        '''Tests if last period date > 16 weeks before report date time validates
        or fails the tests if Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_done': YES,
            'rapid_test_date': get_utcnow().date(),
            'rapid_test_result': None
        }
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('rapid_test_result', form_validator._errors)
