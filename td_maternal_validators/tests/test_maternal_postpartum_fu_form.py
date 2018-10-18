from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO
from ..form_validators import MaternalPostPartumFuFormValidator


@tag('pp')
class TestMaternalPostPartumFuForm(TestCase):
    maternal_hospitalization_cls = apps.get_model(
        'td_maternal.maternalobstericalhistory')

    def test_hospitalized_yes_reason_required(self):
        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': None,
            'hospitalization_days': get_utcnow()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_yes_reason_provided(self):
        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': self.maternal_hospitalization_cls,
            'hospitalization_days': get_utcnow()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hospitalized_no_reason_invalid(self):
        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': 'confidential',
            'hospitalization_days': None}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_no_reason_valid(self):
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

    def test_hospitalized_yes_number_of_days_required(self):
        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': 'confidential',
            'hospitalization_days': None}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_days', form_validator._errors)

    def test_hospitalized_yes_number_of_days_provided(self):
        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': 'confidential',
            'hospitalization_days': None}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
