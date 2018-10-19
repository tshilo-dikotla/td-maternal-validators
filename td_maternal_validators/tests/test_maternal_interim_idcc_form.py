from edc_constants.constants import YES, NO
from django.test import TestCase
from django.core.exceptions import ValidationError
from ..form_validators import MaternalIterimIdccFormValidator
from edc_base.utils import get_utcnow


class TestMaternalInterimIdccFormValidator(TestCase):
    def test_last_visit_is_yes_valid(self):
        '''True if info_since_lastvisit is yes.
        '''
        cleaned_data = {
            "info_since_lastvisit": YES,
            "recent_cd4": 440.5,
            "recent_cd4_date": get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raises. Got{e}')

    def test_last_visit_is_yes_invalid(self):
        '''Assert raises exception if the last visit is yes but recent_cd4 is
        not provided  and recent_c4_date is provided.
        '''
        cleaned_data = {
            "info_since_lastvisit": YES,
            "recent_cd4": None,
            "recent_cd4_date": get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_cd4', form_validator._errors)

    def test_last_visit_is_yes_without_recent_cd4_date(self):
        '''Assert raises exception if the last visit is yes, recent_cd4 has a value but
        recent_cd4_date has not date.
        '''
        cleaned_data = {
            "info_since_lastvisit": YES,
            "recent_cd4": 440.5,
            "recent_cd4_date": None
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_cd4_date', form_validator._errors)

    def test_last_visit_is_no_others_yes(self):
        '''Assert raises exception if the last visit is no, but recent_cd4 and
        recent_cd4_date are given.
        '''
        cleaned_data = {
            "info_since_lastvisit": NO,
            "recent_cd4": 440.5,
            "recent_cd4_date": get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_cd4', form_validator._errors)

    def test_last_visit_is_no_recent_cd4_is_none(self):
        '''Assert raises exception if the last visit is yes, recent_cd4 is none but
        recent_cd4_date has date.
        '''
        cleaned_data = {
            "info_since_lastvisit": NO,
            "recent_cd4": None,
            "recent_cd4_date": get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_cd4_date', form_validator._errors)

    def test_last_visit_is_yes_value_vl_recent_vl_date(self):
        '''Assert raises exception if the last visit is yes, value_vl is given and
        recent_vl_date has date.
        '''
        cleaned_data = {
            "info_since_lastvisit": YES,
            "value_vl": 440.5,
            "recent_vl_date": get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raises. Got{e}')

    def test_last_visit_is_yes_value_vl_none(self):
        '''Assert raises exception if the last visit is yes but recent_vl is
        not provided  and recent_vl_date is provided.
        '''
        cleaned_data = {
            "info_since_lastvisit": YES,
            "value_vl": None,
            "recent_vl_date": get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('value_vl', form_validator._errors)

    def test_last_visit_is_yes_without_recent_vl_date(self):
        '''Assert raises exception if the last visit is yes, recent_vl has a value but
        recent_cd4_date has not date.
        '''
        cleaned_data = {
            "info_since_lastvisit": YES,
            "value_vl": 440.5,
            "recent_vl_date": None
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_vl_date', form_validator._errors)

    def test_last_visit_is_no_others_valid(self):
        '''Assert raises exception if the last visit is no, but other fields are valid
        '''
        cleaned_data = {
            "info_since_lastvisit": NO,
            "value_vl": 440.5,
            "recent_vl_date": get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('value_vl', form_validator._errors)

    def test_last_visit_is_no_recent_vl_is_none(self):
        '''Assert raises exception if the last visit is yes, recent_vl is none but
        recent_vl_date has date.
        '''
        cleaned_data = {
            "info_since_lastvisit": NO,
            "value_vl": None,
            "recent_vl_date": get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_vl_date', form_validator._errors)

    def test_last_visit_is_yes_value_vl_size_less_than(self):
        '''Assert raises exception if the last visit is yes, value_vl_size is less
        but value_vl is invalid.
        '''
        cleaned_data = {
            "info_since_lastvisit": YES,
            "value_vl": 40,
            "value_vl_size": 'less_than'
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raises. Got{e}')
