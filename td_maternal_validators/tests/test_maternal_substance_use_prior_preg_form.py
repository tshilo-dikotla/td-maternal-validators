from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import YES, NO
from ..form_validators import MaternalSubstanceUsePriorPregFormValidator


class TestMaternalSubstanceUsePriorPregForm(TestCase):
    def test_smoked_prior_to_preg_valid(self):
        '''True if smoked_prior_to_preg is Yes and smoking_prior_to_preg_freq is True
        '''
        cleaned_data = {
            "smoked_prior_to_preg": YES,
            "smoking_prior_to_preg_freq": True
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_smoked_prior_to_preg_invalid(self):
        '''Assert raises exception if smoked_prior_to_preg is Yes but smoking_prior_to_
        preg_freq is false.
        '''
        cleaned_data = {
            "smoked_prior_to_preg": YES,
            "smoking_prior_to_preg_freq": False
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('smoking_prior_to_preg_freq', form_validator._errors)

    def test_smoked_prior_to_preg_valid_no(self):
        '''True if smoked_prior_to_preg is NO and smoking_prior_to_preg_freq is False
        '''
        cleaned_data = {
            "smoked_prior_to_preg": NO,
            "smoking_prior_to_preg_freq": False
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_smoked_prior_to_preg_invalid_no(self):
        '''Assert raises exception if smoked_prior_to_preg is NO but smoking_prior_to_
        preg_freq is True.
        '''
        cleaned_data = {
            "smoked_prior_to_preg": NO,
            "smoking_prior_to_preg_freq": True
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('smoking_prior_to_preg_freq', form_validator._errors)

    def test_alcohol_prior_preg_valid(self):
        '''True if alcohol_prior_pregnancy is Yes and alcohol_prior_preg_freq is True
        '''
        cleaned_data = {
            "alcohol_prior_pregnancy": YES,
            "alcohol_prior_preg_freq": True
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_alcohol_prior_preg_invalid(self):
        '''Assert raises exception if alcohol_prior_pregnancy is Yes but
        alcohol_prior_preg_freq is false.
        '''
        cleaned_data = {
            "alcohol_prior_pregnancy": YES,
            "alcohol_prior_preg_freq": False
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('alcohol_prior_preg_freq', form_validator._errors)

    def test_alcohol_prior_pregnancy_valid_no(self):
        '''True if alcohol_prior_pregnancy is NO and alcohol_prior_preg_freq is False
        '''
        cleaned_data = {
            "alcohol_prior_pregnancy": NO,
            "alcohol_prior_preg_freq": False
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_alcohol_prior_pregnancy_invalid_no(self):
        '''Assert raises exception if alcohol_prior_pregnancy is NO but
        alcohol_prior_preg_freq is True.
        '''
        cleaned_data = {
            "alcohol_prior_pregnancy": NO,
            "alcohol_prior_preg_freq": True
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('alcohol_prior_preg_freq', form_validator._errors)

    def test_marijuana_prior_preg_valid(self):
        '''True if marijuana_prior_preg is Yes and marijuana_prior_preg_freq is True
        '''
        cleaned_data = {
            "marijuana_prior_preg": YES,
            "marijuana_prior_preg_freq": True
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_marijuana_prior_preg_invalid(self):
        '''Assert raises exception if smoked_prior_to_preg is Yes but
        marijuana_prior_preg_freq is false.
        '''
        cleaned_data = {
            "marijuana_prior_preg": YES,
            "marijuana_prior_preg_freq": False
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('marijuana_prior_preg_freq', form_validator._errors)

    def test_marijuana_prior_preg_valid_no(self):
        '''True if marijuana_prior_preg is NO and marijuana_prior_preg_freq is False
        '''
        cleaned_data = {
            "marijuana_prior_preg": NO,
            "marijuana_prior_preg_freq": False
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_marijuana_prior_preg_invalid_no(self):
        '''Assert raises exception if marijuana_prior_preg is NO but
        marijuana_prior_preg_freq is True.
        '''
        cleaned_data = {
            "marijuana_prior_preg": NO,
            "marijuana_prior_preg_freq": True
        }
        form_validator = MaternalSubstanceUsePriorPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('marijuana_prior_preg_freq', form_validator._errors)