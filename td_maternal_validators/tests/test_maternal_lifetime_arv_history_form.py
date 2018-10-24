from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import (RESTARTED, NO, YES, CONTINUOUS, STOPPED)
from .models import MaternalConsent, Appointment, MaternalVisit
from ..form_validators import MaternalLifetimeArvHistoryFormValidator


class TestMaternalLifetimeArvHistoryForm(TestCase):
    def setUp(self):
        self.subject_consent = MaternalConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment)

    def test_preg_on_haart_no_preg_prior_invalid(self):
        cleaned_data = {
            'preg_on_haart': NO,
            'prior_preg': RESTARTED}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)

    def test_preg_on_haart_no_preg_prior_invalid2(self):
        cleaned_data = {
            'preg_on_haart': NO,
            'prior_preg': CONTINUOUS}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)

    def test_preg_on_haart_yes_preg_prior_invalid(self):
        cleaned_data = {
            'preg_on_haart': YES,
            'prior_preg': STOPPED,
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': 'yes'}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)

    def test_preg_on_haart_yes_start_date_required(self):
        cleaned_data = {
            'preg_on_haart': YES,
            'haart_start_date': None,
            'is_date_estimated': 'no'}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('haart_start_date', form_validator._errors)

    def test_preg_on_haart_yes_start_date_provided(self):
        cleaned_data = {
            'preg_on_haart': YES,
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': 'no'}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_haart_start_date_valid_date_est_required(self):
        cleaned_data = {
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': None}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_date_estimated', form_validator._errors)

    def test_haart_start_date_valid_date_est_provided(self):
        cleaned_data = {
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': 'yes'}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_haart_start_date_invalid_date_est_invalid(self):
        cleaned_data = {
            'haart_start_date': None,
            'is_date_estimated': 'yes'}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_date_estimated', form_validator._errors)

    def test_haart_start_date_invalid_date_est_valid(self):
        cleaned_data = {
            'haart_start_date': None,
            'is_date_estimated': None}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
