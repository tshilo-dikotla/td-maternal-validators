from django.core.exceptions import ValidationError
from django.test import TestCase
from ..form_validators import MaternalArvFormValidator
from edc_base.utils import get_utcnow
from datetime import timedelta
from edc_constants.constants import YES, NO

from .models import MaternalArvPreg, MaternalArv


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

    def test_took_marternal_arv_yes_valid(self):
        '''True if subject took maternal arv and provides the arv_code
        '''
        maternal_arv_preg = MaternalArvPreg.objects.create(took_arv=YES)
        MaternalArv.objects.create(maternal_arv_preg=maternal_arv_preg)

        cleaned_data = {
            'maternal_arv_preg': maternal_arv_preg,
            "stop_date": get_utcnow().date(),
            "start_date": get_utcnow().date(),
            "arv_code": 'Value',
        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_took_maternal_arv_yes_invalid(self):
        '''Assert raises exception if the took_arv is yes but arv_code is not given
        '''
        maternal_arv_preg = MaternalArvPreg.objects.create(took_arv=YES)
        MaternalArv.objects.create(maternal_arv_preg=maternal_arv_preg)

        cleaned_data = {
            'maternal_arv_preg': maternal_arv_preg,
            "stop_date": get_utcnow().date(),
            "start_date": get_utcnow().date(),
            "arv_code": None,
        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('arv_code', form_validator._errors)

    def test_took_maternal_arv_no_valid(self):
        '''True if took_arv is no and arv_code is none
        '''
        maternal_arv_preg = MaternalArvPreg.objects.create(took_arv=NO)
        MaternalArv.objects.create(maternal_arv_preg=maternal_arv_preg)

        cleaned_data = {
            'maternal_arv_preg': maternal_arv_preg,
            "stop_date": get_utcnow().date(),
            "start_date": get_utcnow().date(),
            "arv_code": None,
        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
