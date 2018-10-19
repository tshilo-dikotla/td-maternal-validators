from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO
from ..form_validators import MaternalPostPartumFuFormValidator

from .models import ListModel


class TestMaternalPostPartumFuForm(TestCase):

    def test_hospitalized_yes_reason_required(self):
        '''Asserts if an exception is raised if subject has been hospitalized
        but the hospitalization reason is missing.'''

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': None,
            'hospitalization_days': get_utcnow()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_yes_reason_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': get_utcnow()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hospitalized_no_reason_invalid(self):
        '''Asserts if an exception is raised if subject has not been hospitalized
        but the hospitalization reason is provided.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')

        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': None}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_yes_number_of_days_required(self):
        '''Asserts if an exception is raised if subject has been hospitalized
        but the hospitalization days are missing.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': None}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_days', form_validator._errors)

    def test_hospitalized_yes_number_of_days_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': get_utcnow().date()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hospitalized_no_number_of_days_invalid(self):
        '''Asserts if an exception is raised if subject has not been hospitalized
        but the hospitalization days are provided.'''

        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': None,
            'hospitalization_days': get_utcnow().date()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_days', form_validator._errors)

    def test_hospitalized_no_valid(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': None,
            'hospitalization_days': None}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
