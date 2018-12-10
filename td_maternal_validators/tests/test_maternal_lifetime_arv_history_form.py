from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import (RESTARTED, NO, YES, CONTINUOUS, STOPPED)
from ..form_validators import MaternalLifetimeArvHistoryFormValidator
from .models import Appointment, MaternalObstericalHistory, MaternalVisit


@tag('life')
class TestMaternalLifetimeArvHistoryForm(TestCase):
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

    @tag('vpp')
    def test_validate_prev_preg_valid(self):
        appointment = Appointment()
        maternal_visit = MaternalVisit(appointment=appointment)
        ob_history = MaternalObstericalHistory(
            maternal_visit=maternal_visit, prev_pregnancies=0)
        print(ob_history.prev_pregnancies)
