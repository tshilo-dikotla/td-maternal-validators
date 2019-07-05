from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import OTHER

from ..form_validators import MaternalDemographicsFormValidator
from .models import MaternalVisit, Appointment
from .models import SubjectScreening, SubjectConsent


class TestMaternaldemographicsForm(TestCase):

    def setUp(self):
        MaternalDemographicsFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        MaternalDemographicsFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        MaternalDemographicsFormValidator.subject_screening_model = \
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

        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_consent.subject_identifier)

    def test_marital_status_other_invalid(self):
        '''Assert raises if marital status was provided as other but
        was not specified in other field.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'marital_status': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('marital_status_other', form_validator._errors)

    def test_marital_status_other_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'marital_status': OTHER,
            'marital_status_other': 'blahblah'
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ethnicity_other_invalid(self):
        '''Assert raises if marital status was provided as other but
        was not specified in other field.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'ethnicity': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ethnicity_other', form_validator._errors)

    def test_ethnicity_other_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'ethnicity': OTHER,
            'ethnicity_other': 'blahblah'
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_current_occupation_other_invalid(self):
        '''Assert raises if marital status was provided as other but
        was not specified in other field.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'current_occupation': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('current_occupation_other', form_validator._errors)

    def test_current_occupation_other_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'current_occupation': OTHER,
            'current_occupation_other': 'blahblah'
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_provides_money_other_invalid(self):
        '''Assert raises if marital status was provided as other but
        was not specified in other field.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'provides_money': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('provides_money_other', form_validator._errors)

    def test_provides_money_other_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'provides_money': OTHER,
            'provides_money_other': 'blahblah'
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_money_earned_other_invalid(self):
        '''Assert raises if marital status was provided as other but
        was not specified in other field.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'money_earned': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('money_earned_other', form_validator._errors)

    def test_money_earned_other_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'money_earned': OTHER,
            'money_earned_other': 'blahblah'
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_toilet_facility_other_invalid(self):
        '''Assert raises if marital status was provided as other but
        was not specified in other field.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'toilet_facility': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('toilet_facility_other', form_validator._errors)

    def test_toilet_facility_other_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'toilet_facility': OTHER,
            'toilet_facility_other': 'blahblah'
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
