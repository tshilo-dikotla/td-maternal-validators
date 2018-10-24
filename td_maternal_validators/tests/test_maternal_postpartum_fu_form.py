from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import (YES, NO, NOT_APPLICABLE)
from .models import MaternalConsent, MaternalVisit,  ListModel
from ..form_validators import MaternalPostPartumFuFormValidator


class TestMaternalPostPartumFuForm(TestCase):
    def Setup(self):
        self.subject_consent = MaternalConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment)

    def test_hospitalized_yes_reason_required(self):
        '''Asserts if an exception is raised if subject has been hospitalized
        but the hospitalization reason is missing.'''

        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': None,
            'hospitalization_days': get_utcnow(),
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_yes_reason_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(
                name='hypertension'),
            'hospitalization_days': get_utcnow(),
            'diagnoses': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hospitalized_yes_reason_na_invalid(self):
        '''Asserts if an exception is raised if subject has been hospitalized
        but the hospitalization reason list selection is N/A.'''

        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': get_utcnow(),
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_no_reason_na_valid(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': None,
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hospitalized_no_reason_list_invalid(self):
        '''Asserts if an exception is raised if subject has not been hospitalized
        but the hospitalization reason is provided.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': None,
            'diagnoses': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_yes_number_of_days_required(self):
        '''Asserts if an exception is raised if subject has been hospitalized
        but the hospitalization days are missing.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(
                name='hypertension'),
            'hospitalization_days': None,
            'diagnoses': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_days', form_validator._errors)

    def test_hospitalized_yes_number_of_days_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(
                name='hypertension'),
            'hospitalization_days': get_utcnow().date(),
            'diagnoses': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hospitalized_no_number_of_days_invalid(self):
        '''Asserts if an exception is raised if subject has not been hospitalized
        but the hospitalization days are provided.'''

        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': get_utcnow().date(),
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_days', form_validator._errors)

    def test_hospitalized_no_number_of_days_valid(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': None,
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diagnoses_required(self):
        '''Asserts if an exception is raised if required field diagnoses
        is missing.'''

        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalization_reason': ListModel.objects.all(),
            'diagnoses': None}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diagnoses', form_validator._errors)

    def test_new_diagnoses_yes_diagnoses_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(name='cancer', short_name='cancer')
        ListModel.objects.create(name='sick', short_name='sick')
        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(name='sick'),
            'hospitalization_days': get_utcnow().date(),
            'new_diagnoses': YES,
            'diagnoses': ListModel.objects.filter(name='cancer')}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_new_diagnoses_yes_diagnosis_na_invalid(self):
        '''Asserts if an exception is raised if new diagnoses is yes
        but the diagnoses list selection is N/A.'''

        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        ListModel.objects.create(name='sick', short_name='sick')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(name='sick'),
            'hospitalization_days': get_utcnow().date(),
            'new_diagnoses': YES,
            'diagnoses': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diagnoses', form_validator._errors)

    def test_new_diagnoses_no_diagnoses_na_valid(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(name='Not Applicable', short_name='N/A')

        cleaned_data = {
            'hospitalization_reason': ListModel.objects.all(),
            'new_diagnoses': NO,
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diagnoses_no_diagnoses_list_invalid(self):
        '''Asserts if an exception is raised if new diagnoses is No
        but the diagnoses list selection includes N/A.'''

        ListModel.objects.create(name='cancer', short_name='cancer')
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalization_reason': ListModel.objects.filter(
                name=NOT_APPLICABLE),
            'new_diagnoses': NO,
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diagnoses', form_validator._errors)
