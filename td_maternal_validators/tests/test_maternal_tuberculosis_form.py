from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import YES, NO
from ..form_validators import MaternalTuberculosisHistoryFormValidator


class TestMaternalSubstanceDuringPregForm(TestCase):

    def setUp(self):
        self.cleaned_data = {
            'coughing': YES,
        }
        pass

    def test_coughing_relation_required(self):
        '''True if coughing is Yes and coughing_rel is provided.'''
        cleaned_data = {
            'coughing': YES,
            'coughing_rel': 'me'
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_coughing_relation_not_required(self):
        '''Assert raises exception if coughing is No but coughing_rel is provided.'''
        cleaned_data = {
            'coughing': NO,
            'coughing_rel': 'me'
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('coughing_rel', form_validator._errors)

    def test_coughing_relation_no_not_required(self):
        '''True if coughing is NO and coughing_rel is not provided.'''
        cleaned_data = {
            'coughing': NO,
            'coughing_rel': None
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_coughing_relation_required_not_provided(self):
        '''Assert raises exception if coughing is Yes but
        coughing_rel is not provided.'''
        cleaned_data = {
            'coughing': YES,
            'coughing_rel': None
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('coughing_rel', form_validator._errors)

    def test_diagnosis_relation_required(self):
        '''True if diagnosis is Yes and diagnosis_rel is provided.'''
        cleaned_data = {
            'diagnosis': YES,
            'diagnosis_rel': 'me'
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diagnosis_relation_not_required(self):
        '''Assert raises exception if diagnosis is NO but diagnosis_rel is provided.'''
        cleaned_data = {
            'diagnosis': NO,
            'diagnosis_rel': 'me'
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diagnosis_rel', form_validator._errors)

    def test_diagnosis_relation_no_not_required(self):
        '''True if diagnosis is NO and diagnosis_rel is not provided.'''
        cleaned_data = {
            'diagnosis': NO,
            'diagnosis_rel': None
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diagnosis_relation_required_not_provided(self):
        '''Assert raises exception if diagnosis is Yes but diagnosis_rel
        is not provided.'''
        cleaned_data = {
            'diagnosis': YES,
            'diagnosis_rel': None
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diagnosis_rel', form_validator._errors)

    def test_tuberculosis_treatment_relation_required(self):
        '''True if tb_treatment is Yes and tb_treatment_rel is provided.'''
        cleaned_data = {
            'tb_treatment': YES,
            'tb_treatment_rel': 'me'
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_tuberculosis_treatment_relation_not_required(self):
        '''Assert raises exception if tb_treatment is NO but tb_treatment_rel
        is provided.'''
        cleaned_data = {
            'tb_treatment': NO,
            'tb_treatment_rel': 'me'
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('tb_treatment_rel', form_validator._errors)

    def test_tuberculosis_treatment_relation_no_not_required(self):
        '''True if tb_treatment is Yes and tb_treatment_rel is provided.'''
        cleaned_data = {
            'tb_treatment': NO,
            'tb_treatment_rel': None
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_tuberculosis_treatment_relation_required_not_provided(self):
        '''Assert raises exception if tb_treatment is NO but tb_treatment_rel
        is provided.'''
        cleaned_data = {
            'tb_treatment': YES,
            'tb_treatment_rel': None
        }
        form_validator = MaternalTuberculosisHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('tb_treatment_rel', form_validator._errors)
