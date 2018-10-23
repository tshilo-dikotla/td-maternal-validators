from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from ..form_validators import MaternalArvPregFormValidator


class TestMaternalArvPregForm(TestCase):
    def test_medication_interrupted_invalid(self):
        '''Assert raises if arvs was interrupted but
        no reasons were given.
        '''
        cleaned_data = {
            "is_interrupt": YES,
            "interrupt": 'reason',
        }
        form_validator = MaternalArvPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_medication_interrupted_invalid_yes(self):
        '''Assert raises if arvs was interrupted but
        no reason was given.
        '''
        cleaned_data = {
            "is_interrupt": YES,
            "interrupt": NOT_APPLICABLE,
        }
        form_validator = MaternalArvPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('interrupt', form_validator._errors)

    def test_medication_interrupted_valid(self):
        '''True if arvs was not interrupted and no
        interrupt reason was provided.
        '''
        cleaned_data = {
            "is_interrupt": NO,
            "interrupt": NOT_APPLICABLE,
        }
        form_validator = MaternalArvPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised. Got {e}')

    def test_medication_interrupted_invalid_none(self):
        '''Assert raises if no interruptions but
        reason is given.
        '''
        cleaned_data = {
            "is_interrupt": NO,
            "interrupt": 'reason',
        }
        form_validator = MaternalArvPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('interrupt', form_validator._errors)
