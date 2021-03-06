from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import (YES, NO, NOT_APPLICABLE)

from td_maternal.models.list_models import Contraceptives

from ..form_validators import MaternalContraceptionFormValidator
from .models import MaternalVisit, Appointment
from .models import SubjectScreening, SubjectConsent


class TestMaternalContraceptionForm(TestCase):

    def setUp(self):
        MaternalContraceptionFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        MaternalContraceptionFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        MaternalContraceptionFormValidator.subject_screening_model = \
            'td_maternal_validators.subjectscreening'

        self.subject_identifier = '11111111'

        self.subject_screening = SubjectScreening.objects.create(
            subject_identifier='11111111',
            screening_identifier='ABC12345',
            age_in_years=22)

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')

        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_consent.subject_identifier)

        Contraceptives.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        Contraceptives.objects.create(name='pills', short_name='Pills')

    def test_more_children_yes_next_child_required(self):
        '''Asserts raises exception if subject wants more children and
        required next child field value is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'more_children': YES,
            'next_child': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('next_child', form_validator._errors)

    def test_more_children_yes_next_child_provided(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'more_children': YES,
            'next_child': 'within 2years'}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_more_children_no_next_child_invalid(self):
        '''Asserts raises exception if subject does not want more
        children and next child field value is provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'more_children': NO,
            'next_child': 'within 2years'}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('next_child', form_validator._errors)

    def test_more_children_no_next_child_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'more_children': NO,
            'next_child': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_uses_contraceptive_yes_method_required(self):
        '''Asserts raises exception if uses contraceptive is yes and
        required contraceptive method is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'uses_contraceptive': YES,
            'contr': Contraceptives.objects.filter(name=NOT_APPLICABLE),
            'contraceptive_startdate': get_utcnow().date}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contr', form_validator._errors)

    def test_uses_contraceptive_no_method_invalid(self):
        '''Asserts raises exception if uses contraceptive is no and
        contraceptive method is provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'uses_contraceptive': NO,
            'contr': Contraceptives.objects.filter(name='pills')}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contr', form_validator._errors)

    def test_uses_contraceptive_no_method_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'uses_contraceptive': NO,
            'contr': Contraceptives.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_uses_contraceptive_yes_startdate_required(self):
        '''Asserts raises exception if uses contraceptive is yes and
        required start date is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'uses_contraceptive': YES,
            'contr': Contraceptives.objects.filter(name='pills'),
            'contraceptive_startdate': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contraceptive_startdate', form_validator._errors)

    def test_uses_contraceptive_no_startdate_invalid(self):
        '''Asserts raises exception if uses contraceptive is no and
        start date is provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'uses_contraceptive': NO,
            'contr': Contraceptives.objects.filter(name=NOT_APPLICABLE),
            'contraceptive_startdate': get_utcnow().date()}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contraceptive_startdate', form_validator._errors)

    def test_uses_contraceptive_no_startdate_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'uses_contraceptive': NO,
            'contr': Contraceptives.objects.filter(name=NOT_APPLICABLE),
            'contraceptive_startdate': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pregancy_yes_pregnancy_date_required(self):
        '''Asserts raises exception if subject is pregnant and
        required pregnancy date is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'another_pregnancy': YES,
            'pregnancy_date': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pregnancy_date', form_validator._errors)

    def pregnancy_yes_pregnancy_date_provided(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'another_pregnancy': YES,
            'pregnancy_date': get_utcnow().date()}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def pregnancy_no_pregancy_date_invalid(self):
        '''Asserts raises exception if subject is not pregnant and
        pregnancy date is provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'another_pregnancy': NO,
            'pregnancy_date': get_utcnow().date()}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pregnancy_date', form_validator._errors)

    def pregnancy_no_pregnancy_date_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'another_pregnancy': NO,
            'pregnancy_date': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pap_smear_yes_pap_smear_date_required(self):
        '''Asserts raises exception if subject had a pap smear and
        date of the pap smear is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear': YES,
            'pap_smear_date': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pap_smear_date', form_validator._errors)

    def test_pap_smear_yes_pap_smear_date_provided(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear': YES,
            'pap_smear_date': get_utcnow().date()}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pap_smear_no_pap_smear_date_invalid(self):
        '''Asserts raises exception if subject did not have a pap smear and
        the pap smear date is provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear': NO,
            'pap_smear_date': get_utcnow().date()}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pap_smear_date', form_validator._errors)

    def test_pap_smear_no_pap_smear_date_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear': NO,
            'pap_smear_date': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pap_smear_result_yes_status_required(self):
        '''Asserts raises exception if pap smear result is yes and
        pap smear result status is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear_result': YES,
            'pap_smear_result_status': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pap_smear_result_status', form_validator._errors)

    def test_pap_smear_result_yes_status_provided(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear_result': YES,
            'pap_smear_result_status': 'Normal'}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pap_smear_result_no_status_invalid(self):
        '''Asserts raises exception if pap smear result is no and
        pap smear result status is provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear_result': NO,
            'pap_smear_result_status': 'Normal'}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pap_smear_result_status', form_validator._errors)

    def test_pap_smear_result_no_status_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear_result': NO,
            'pap_smear_result_status': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pap_smear_status_abnormal_result_abn_required(self):
        '''Asserts raises exception if pap smear result status is abnormal and
        abnormal pap smear result details is missing.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear_result_status': 'abnormal',
            'pap_smear_result_abnormal': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pap_smear_result_abnormal', form_validator._errors)

    def test_pap_smear_status_abnormal_result_abn_provided(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear_result_status': 'abnormal',
            'pap_smear_result_abnormal': 'some important stuff.'}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pap_smear_status_normal_result_abn_invalid(self):
        '''Asserts raises exception if pap smear result status is normal and
        abnormal pap smear result details is provided.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear_result_status': 'normal',
            'pap_smear_result_abnormal': 'some important stuff.'}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pap_smear_result_abnormal', form_validator._errors)

    def test_pap_smear_status_normal_result_abn_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'pap_smear_result_status': 'normal',
            'pap_smear_result_abnormal': None}
        form_validator = MaternalContraceptionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
