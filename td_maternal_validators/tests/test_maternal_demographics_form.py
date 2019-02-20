from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import OTHER
from ..form_validators import MaternalDemographicsFormValidator


class TestMaternaldemographicsForm(TestCase):

    def test_marital_status_other_invalid(self):
        '''Assert raises if marital status was provided as other but
        was not specified in other field.
        '''
        cleaned_data = {
            'marital_status': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('marital_status_other', form_validator._errors)

    def test_marital_status_other_valid(self):
        cleaned_data = {
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
            'ethnicity': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ethnicity_other', form_validator._errors)

    def test_ethnicity_other_valid(self):
        cleaned_data = {
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
            'current_occupation': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('current_occupation_other', form_validator._errors)

    def test_current_occupation_other_valid(self):
        cleaned_data = {
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
            'provides_money': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('provides_money_other', form_validator._errors)

    def test_provides_money_other_valid(self):
        cleaned_data = {
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
            'money_earned': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('money_earned_other', form_validator._errors)

    def test_money_earned_other_valid(self):
        cleaned_data = {
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
            'toilet_facility': OTHER,
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('toilet_facility_other', form_validator._errors)

    def test_toilet_facility_other_valid(self):
        cleaned_data = {
            'toilet_facility': OTHER,
            'toilet_facility_other': 'blahblah'
        }
        form_validator = MaternalDemographicsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
