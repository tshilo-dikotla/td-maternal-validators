from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, POS, NEG, IND, NO
from ..form_validators import RapidTestResultFormValidator


@tag('rr')
class TestRapidTestResultForm(TestCase):

    def test_rapid_test_done_YES_result_date_required(self):
        cleaned_data = {
            'rapid_test_done': YES,
            'result_date': None,
            'result': POS or NEG or IND}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('result_date', form_validator._errors)

    def test_rapid_test_done_YES_result_date_provided(self):
        cleaned_data = {
            'rapid_test_done': YES,
            'result_date': get_utcnow().date(),
            'result': POS or NEG or IND}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_rapid_test_done_YES_result_required(self):
        cleaned_data = {
            'rapid_test_done': YES,
            'result_date': get_utcnow().date(),
            'result': None}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('result', form_validator._errors)

    def test_rapid_test_done_YES_result_valid(self):
        cleaned_data = {
            'rapid_test_done': YES,
            'result_date': get_utcnow().date(),
            'result': POS or NEG or IND}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_rapid_test_done_NO_result_date_invalid(self):
        cleaned_data = {
            'rapid_test_done': NO,
            'result_date': get_utcnow().date()}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('result_date', form_validator._errors)

    def test_rapid_test_done_NO_result_date_valid(self):
        cleaned_data = {
            'rapid_test_done': NO,
            'result_date': None}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_rapid_test_done_NO_result_invalid(self):
        cleaned_data = {
            'rapid_test_done': NO,
            'result': POS or NEG or IND}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('result', form_validator._errors)

    def test_rapid_test_done_NO_result_valid(self):
        cleaned_data = {
            'rapid_test_done': NO,
            'result': None}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
