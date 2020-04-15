import datetime
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import MaternalCovidScreeningFormValidator
from .models import SubjectConsent, MaternalVisit, Appointment


@tag('cv')
class TestMaternalCovidScreeningForm(TestCase):

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow())

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2010')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,)

    def test_form_is_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': NO,
            'household_positive': NO}
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_covid_tested_invalid1(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': YES,
            'household_positive': NO,
            'is_test_date_estimated': NO,
            'covid_results': 'blahblah'}
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('covid_test_date', form_validator._errors)

    def test_covid_tested_invalid2(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': YES,
            'household_positive': NO,
            'covid_test_date': get_utcnow().date(),
            'covid_results': 'blahblah'}
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_test_date_estimated', form_validator._errors)

    def test_covid_tested_invalid3(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': YES,
            'covid_test_date': get_utcnow().date(),
            'household_positive': NO,
            'is_test_date_estimated': NO, }
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('covid_results', form_validator._errors)

    def test_covid_tested_invalid4(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': NO,
            'covid_test_date': get_utcnow().date(),
            'household_positive': NO}
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('covid_test_date', form_validator._errors)

    def test_covid_tested_invalid5(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': NO,
            'household_positive': NO,
            'is_test_date_estimated': NO,
            'covid_results': 'blahblah'}
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_test_date_estimated', form_validator._errors)

    def test_covid_tested_invalid6(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': NO,
            'household_positive': NO,
            'covid_results': 'blahblah'}
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('covid_results', form_validator._errors)

    def test_covid_tested_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': YES,
            'covid_test_date': get_utcnow().date(),
            'household_positive': NO,
            'is_test_date_estimated': NO,
            'covid_results': 'blahblah'}
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_covid_test_date_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': YES,
            'covid_test_date': datetime.date(2019, 12, 1),
            'household_positive': NO,
            'is_test_date_estimated': NO,
            'covid_results': 'blahblah'}
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('covid_test_date', form_validator._errors)

    def test_household_test_date_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': NO,
            'household_test_date': datetime.date(2019, 12, 1),
            'household_positive': YES,
            'is_household_test_estimated': NO}
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('household_test_date', form_validator._errors)

    def test_is_test_date_estimated_invalid1(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': NO,
            'household_test_date': get_utcnow().date(),
            'household_positive': YES, }
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_household_test_estimated', form_validator._errors)

    def test_is_test_date_estimated_invalid2(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'covid_tested': NO,
            'household_positive': NO,
            'is_household_test_estimated': NO, }
        form_validator = MaternalCovidScreeningFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_household_test_estimated', form_validator._errors)
