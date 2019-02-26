from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from ..form_validators import MaternalUltrasoundInitialFormValidator


class TestMaternalUltrasoundInitialForm(TestCase):

    def test_est_ultrasound_lesss_than(self):
        cleaned_data = {
            'est_edd_ultrasound': get_utcnow().date() + relativedelta(days=50),
            'report_datetime': get_utcnow()
        }
        form_validator = MaternalUltrasoundInitialFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_est_ultrasound_greater_than(self):
        cleaned_data = {
            'est_edd_ultrasound': get_utcnow().date() + relativedelta(weeks=60),
            'report_datetime': get_utcnow(),
        }
        form_validator = MaternalUltrasoundInitialFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('est_edd_ultrasound', form_validator._errors)

    def test_est_ultrasound_less_than_invalid(self):
        cleaned_data = {
            'est_edd_ultrasound': get_utcnow().date(),
            'report_datetime': get_utcnow()
        }
        form_validator = MaternalUltrasoundInitialFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ga_ultrasound_wks_valid(self):
        cleaned_data = {
            'ga_by_ultrasound_wks': 35,
            'report_datetime': get_utcnow(),
            'est_edd_ultrasound': get_utcnow().date() + relativedelta(weeks=5),

        }
        form_validator = MaternalUltrasoundInitialFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ga_ultrasound_wks_invalid(self):
        cleaned_data = {
            'ga_by_ultrasound_wks': 50,
            'report_datetime': get_utcnow(),
        }
        form_validator = MaternalUltrasoundInitialFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ga_by_ultrasound_wks', form_validator._errors)

    def test_ga_by_ultrasound_days_valid(self):
        cleaned_data = {
            'ga_by_ultrasound_days': 6,
            'report_datetime': get_utcnow(),
        }
        form_validator = MaternalUltrasoundInitialFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ga_by_ultrasound_against_est_edd_ultrasound_valid(self):
        cleaned_data = {
            'est_edd_ultrasound': get_utcnow().date() + relativedelta(weeks=5),
            'ga_by_ultrasound_wks': 35,
            'report_datetime': get_utcnow()
        }
        form_validator = MaternalUltrasoundInitialFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
