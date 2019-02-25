from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import MaternalIterimIdccFormValidator


@tag('idcc')
class TestMaternalInterimIdccFormValidator(TestCase):

    def test_last_visit_is_no_recent_cd4_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': NO,
            'recent_cd4': 250.2,
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_cd4', form_validator._errors)

    def test_last_visit_is_no_recent_cd4_date_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': NO,
            'recent_cd4_date': get_utcnow(),
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_cd4_date', form_validator._errors)

    def test_last_visit_is_no_value_vl_size_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': NO,
            'value_vl_size': 'equal',
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('value_vl_size', form_validator._errors)

    def test_last_visit_is_no_value_vl_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': NO,
            'value_vl': 440.5,
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('value_vl', form_validator._errors)

    def test_last_visit_is_no_recent_vl_date_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': NO,
            'recent_vl_date': get_utcnow(),
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_vl_date', form_validator._errors)

    def test_last_visit_is_no_valid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': NO,
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raises. Got{e}')

    def test_recent_cd4_no_date_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'recent_cd4': 250.2,
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_cd4_date', form_validator._errors)

    def test_recent_cd4_date_valid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'recent_cd4': 250.2,
            'recent_cd4_date': get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raises. Got{e}')

    def test_value_vl_no_value_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'recent_cd4': None,
            'value_vl_size': 'equal',
            'value_vl': 250.2,
            'recent_vl_date': None
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recent_vl_date', form_validator._errors)

    def test_value_vl_value_valid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'value_vl_size': 'equal',
            'value_vl': 4444,
            'recent_vl_date': get_utcnow()
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raises. Got{e}')

    def test_value_vl_no_less_than_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'value_vl': 250.2,
            'recent_vl_date': get_utcnow(),
            'value_vl_size': 'less_than'
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('value_vl', form_validator._errors)

    def test_value_vl_no_less_than_valid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'value_vl': 400,
            'recent_vl_date': get_utcnow(),
            'value_vl_size': 'less_than'
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raises. Got{e}')

    def test_value_vl_no_greater_than_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'value_vl': 250.2,
            'recent_vl_date': get_utcnow(),
            'value_vl_size': 'greater_than'
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('value_vl', form_validator._errors)

    def test_value_vl_no_greater_than_valid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'value_vl': 750000,
            'recent_vl_date': get_utcnow(),
            'value_vl_size': 'greater_than'
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raises. Got{e}')

    def test_value_vl_no_equal_invalid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'value_vl': 250.2,
            'recent_vl_date': get_utcnow(),
            'value_vl_size': 'equal'
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('value_vl', form_validator._errors)

    def test_value_vl_no_equal_valid(self):
        '''Assert raises exception if the last visit is no,
        but other fields are provided.
        '''
        cleaned_data = {
            'info_since_lastvisit': YES,
            'value_vl': 6000,
            'recent_vl_date': get_utcnow(),
            'value_vl_size': 'equal'
        }
        form_validator = MaternalIterimIdccFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raises. Got{e}')
