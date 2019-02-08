from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, NEG, YES

from ..form_validators import AntenatalEnrollmentFormValidator
from .models import (AntenatalEnrollment, SubjectScreening,
                     SubjectConsent, TdConsentVersion)


@tag('enrol')
class TestAntenatalEnrollmentForm(TestCase):

    def setUp(self):
        AntenatalEnrollmentFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        AntenatalEnrollmentFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        AntenatalEnrollmentFormValidator.subject_screening_model = \
            'td_maternal_validators.subjectscreening'
        AntenatalEnrollmentFormValidator.antenatal_enrollment_model = \
            'td_maternal_validators.antenatalenrollment'

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

        self.antenatal_enrollment = AntenatalEnrollment.objects.create(
            subject_identifier='11111111',
            enrollment_hiv_status=NEG, week32_result=POS,
            rapid_test_done=YES,
            rapid_test_result=POS, rapid_test_date=get_utcnow().date())

    def test_LMP_within_16wks_of_report_datetime_invalid(self):
        '''Asserts if an exception is raised if last period date is within
        16 weeks of the report datetime.'''

        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'report_datetime': get_utcnow(),
            'last_period_date': get_utcnow().date() - relativedelta(weeks=2),
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
            'rapid_test_date': get_utcnow()
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
            'rapid_test_date': get_utcnow()
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
            'rapid_test_date': get_utcnow()
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
            'rapid_test_date': get_utcnow()
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
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
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
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
            'rapid_test_date': get_utcnow()
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
            'report_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'rapid_test_date': get_utcnow().date() - relativedelta(days=3),
            'rapid_test_done': YES,
            'rapid_test_result': NEG}
        form_validator = AntenatalEnrollmentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
