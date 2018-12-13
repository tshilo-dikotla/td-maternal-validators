from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from ..form_validators import MaternalHivInterimHxFormValidator


@tag('interim')
class TestMaternalHivInterimHxForm(TestCase):

    def test_has_cd4_YES_cd4_date_required(self):
        cleaned_data = {
            'has_cd4': YES,
            'cd4_date': None,
            'cd4_result': '600'
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('cd4_date', form_validator._errors)

    def test_has_cd4_YES_cd4_date_provided(self):
        cleaned_data = {
            'has_cd4': YES,
            'cd4_date': get_utcnow().date(),
            'cd4_result': '600'
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_has_cd4_YES_cd4_result_required(self):
        cleaned_data = {
            'has_cd4': YES,
            'cd4_date': get_utcnow().date(),
            'cd4_result': None
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('cd4_result', form_validator._errors)

    def test_has_cd4_YES_cd4_result_provided(self):
        cleaned_data = {
            'has_cd4': YES,
            'cd4_date': get_utcnow().date(),
            'cd4_result': '600'
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_has_cd4_NO_cd4_date_valid(self):
        cleaned_data = {
            'has_cd4': NO,
            'cd4_date': None,
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_has_cd4_NO_cd4_date_invalid(self):
        cleaned_data = {
            'has_cd4': NO,
            'cd4_date': get_utcnow().date(),
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('cd4_date', form_validator._errors)

    def test_has_cd4_NO_cd4_result_valid(self):
        cleaned_data = {
            'has_cd4': NO,
            'cd4_result': None
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_has_cd4_NO_cd4_result_invalid(self):
        cleaned_data = {
            'has_cd4': NO,
            'cd4_result': '600'
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('cd4_result', form_validator._errors)

    def test_has_vl_YES_vl_date_required(self):
        cleaned_data = {
            'has_vl': YES,
            'vl_date': None}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_date', form_validator._errors)

    def test_has_vl_YES_vl_date_provided(self):
        cleaned_data = {
            'has_vl': YES,
            'vl_date': get_utcnow().date()}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_has_vl_YES_vl_detectable_applicable(self):
        cleaned_data = {
            'has_vl': YES,
            'vl_date': get_utcnow().date(),
            'vl_detectable': NOT_APPLICABLE}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_detectable', form_validator._errors)

    def test_has_vl_YES_vl_detectable_provided(self):
        cleaned_data = {
            'has_vl': YES,
            'vl_date': get_utcnow().date(),
            'vl_detectable': YES,
            'vl_result': '600'}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_has_vl_NO_vl_date_valid(self):
        cleaned_data = {
            'has_vl': NO,
            'vl_date': None}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_has_vl_NO_vl_date_invalid(self):
        cleaned_data = {
            'has_vl': NO,
            'vl_date': get_utcnow().date()}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_date', form_validator._errors)

    def test_has_vl_NO_vl_detectable_NA(self):
        cleaned_data = {
            'has_vl': NO,
            'vl_detectable': NOT_APPLICABLE}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_has_vl_NO_vl_detectable_invalid(self):
        cleaned_data = {
            'has_vl': NO,
            'vl_detectable': YES}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_detectable', form_validator._errors)

    def test_vl_detectable_YES_vl_result_required(self):
        cleaned_data = {
            'has_vl': YES,
            'vl_date': get_utcnow().date(),
            'vl_detectable': YES,
            'vl_result': None}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_result', form_validator._errors)

    def test_vl_detectable_YES_vl_result_provided(self):
        cleaned_data = {
            'has_vl': YES,
            'vl_date': get_utcnow().date(),
            'vl_detectable': YES,
            'vl_result': '600'}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_vl_detectable_NO_vl_result_invalid(self):
        cleaned_data = {
            'has_vl': YES,
            'vl_date': get_utcnow().date(),
            'vl_detectable': NO,
            'vl_result': '600'}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_result', form_validator._errors)

    def test_vl_detectable_NO_vl_result_valid(self):
        cleaned_data = {
            'has_vl': YES,
            'vl_date': get_utcnow().date(),
            'vl_detectable': NO,
            'vl_result': None}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
