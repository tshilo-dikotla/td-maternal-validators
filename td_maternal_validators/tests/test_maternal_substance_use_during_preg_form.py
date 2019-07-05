from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import MaternalSubstanceUseDuringPregFormValidator
from .models import SubjectConsent, MaternalVisit, Appointment


class TestMaternalSubstanceDuringPregForm(TestCase):

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow())

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,)

    def test_smoked_during_preg_yes_freq_required(self):
        '''Asserts raises exception if subject smoked during pregnancy and
        required smoking frequency value is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'smoked_during_pregnancy': YES,
            'smoking_during_preg_freq': None}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('smoking_during_preg_freq', form_validator._errors)

    def test_smoked_during_preg_yes_freq_provided(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'smoked_during_pregnancy': YES,
            'smoking_during_preg_freq': 'daily'}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_smoked_during_preg_no_freq_invalid(self):
        '''Asserts raises exception if subject did not smoke during pregnancy
        and smoking frequency value has been provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'smoked_during_pregnancy': NO,
            'smoking_during_preg_freq': 'daily'}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('smoking_during_preg_freq', form_validator._errors)

    def test_smoked_during_preg_no_freq_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'smoked_during_pregnancy': NO,
            'smoking_during_preg_freq': None}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_alcohol_during_preg_yes_freq_required(self):
        '''Asserts raises exception if subject drank alcohol during pregnancy
        and required alcohol drinking frequency value is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'alcohol_during_pregnancy': YES,
            'alcohol_during_preg_freq': None}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('alcohol_during_preg_freq', form_validator._errors)

    def test_alcohol_during_preg_yes_freq_provided(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'alcohol_during_pregnancy': YES,
            'alcohol_during_preg_freq': 'weekly'}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_alcohol_during_preg_no_freq_invalid(self):
        '''Asserts raises exception if subject did not drink alcohol during
        pregnancy and drinking frequency value has been provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'alcohol_during_pregnancy': NO,
            'alcohol_during_preg_freq': 'weekly'}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('alcohol_during_preg_freq', form_validator._errors)

    def test_alcohol_during_preg_no_freq_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'alcohol_during_pregnancy': NO,
            'alcohol_during_preg_freq': None}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_marijuana_during_preg_yes_freq_required(self):
        '''Asserts raises exception if subject smoked weed during pregnancy
        and required weed smoking frequency value is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'marijuana_during_preg': YES,
            'marijuana_during_preg_freq': None}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('marijuana_during_preg_freq', form_validator._errors)

    def test_marijuana_during_preg_yes_freq_provided(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'marijuana_during_preg': YES,
            'marijuana_during_preg_freq': 'daily'}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_marijuana_during_preg_no_freq_invalid(self):
        '''Asserts raises exception if subject did not smoke weed during
        pregnancy and weed smoking frequency value is provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'marijuana_during_preg': NO,
            'marijuana_during_preg_freq': 'weekly'}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('marijuana_during_preg_freq', form_validator._errors)

    def test_marijuana_during_preg_no_freq_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'marijuana_during_preg': NO,
            'marijuana_during_preg_freq': None}
        form_validator = MaternalSubstanceUseDuringPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
