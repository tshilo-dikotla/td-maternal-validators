from django.core.exceptions import ValidationError
from django.test import TestCase
from ..form_validators import MaternalClinicalMeasurememtsOneFormValidator


class TestMaternalClinicalTestOneForm(TestCase):
    def test_systolic_bp_yes_valid(self):
        '''True if systolic_bp is selected
        '''
        cleaned_data = {
            "systolic_bp": 30,
            "diastolic_bp": 20,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_systolic_bp_yes_invalid(self):
        '''Assert raises exception if systolic_bp
        is not selected.
        '''
        cleaned_data = {
            "systolic_bp": None,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('systolic_bp', form_validator._errors)

    def test_diastolic_bp_yes_valid(self):
        '''True if diastolic_bp is selected
        '''
        cleaned_data = {
            "systolic_bp": 50,
            "diastolic_bp": 40,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diastolic_bp_yes_invalid(self):
        '''Assert raises exception if diastolic_bp
        is not selected.
        '''
        cleaned_data = {
            "diastolic_bp": None,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diastolic_bp', form_validator._errors)

    def test_systolic_bp_less_invalid(self):
        '''Assert raises exception if systolic_bp
        is < diastolic_bp.
        '''
        cleaned_data = {
            "systolic_bp": 20,
            "diastolic_bp": 40,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diastolic_bp', form_validator._errors)

    def test_systolic_bp_greater_valid(self):
        '''True if diastolic_bp is selected
        '''
        cleaned_data = {
            "systolic_bp": 50,
            "diastolic_bp": 40,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
