from django.core.exceptions import ValidationError
from django.test import TestCase
from ..form_validators import MaternalArvFormValidator
from edc_base.utils import get_utcnow
from datetime import timedelta


class TestMaternalArvPregForm(TestCase):
    def test_stop_date_invalid(self):
        '''Assert Raises if start_date is > stop_date.
        '''
        cleaned_data = {
            "stop_date": get_utcnow().date(),
            "start_date": get_utcnow().date() + timedelta(days=30),
            }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('start_date', form_validator._errors)

    def test_stop_date_valid(self):
        '''True if start_date < stop_date.
        '''
        cleaned_data = {
            "stop_date": get_utcnow().date() + timedelta(days=30),
            "start_date": get_utcnow().date()
            }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_stop_date_equals_invalid(self):
        '''Invalid because we need stop_date > start_date.
        '''
        cleaned_data = {
            "stop_date": get_utcnow().date(),
            "start_date": get_utcnow().date(),
            }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
