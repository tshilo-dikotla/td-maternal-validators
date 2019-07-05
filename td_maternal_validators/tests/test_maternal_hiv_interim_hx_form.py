from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE

from ..form_validators import MaternalHivInterimHxFormValidator
from .models import MaternalVisit, Appointment
from .models import SubjectScreening, SubjectConsent


class TestMaternalHivInterimHxForm(TestCase):

    def setUp(self):
        MaternalHivInterimHxFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        MaternalHivInterimHxFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        MaternalHivInterimHxFormValidator.subject_screening_model = \
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

    def test_has_cd4_YES_cd4_date_required(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
            'has_cd4': NO,
            'cd4_date': get_utcnow().date(),
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('cd4_date', form_validator._errors)

    def test_has_cd4_NO_cd4_result_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
            'has_cd4': NO,
            'cd4_result': '600'
        }
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('cd4_result', form_validator._errors)

    def test_has_vl_YES_vl_date_required(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'has_vl': YES,
            'vl_date': None}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_date', form_validator._errors)

    def test_has_vl_YES_vl_date_provided(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
            'has_vl': YES,
            'vl_date': get_utcnow().date(),
            'vl_detectable': NOT_APPLICABLE}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_detectable', form_validator._errors)

    def test_has_vl_YES_vl_detectable_provided(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
            'has_vl': NO,
            'vl_date': get_utcnow().date()}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_date', form_validator._errors)

    def test_has_vl_NO_vl_detectable_NA(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
            'has_vl': NO,
            'vl_detectable': YES}
        form_validator = MaternalHivInterimHxFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('vl_detectable', form_validator._errors)

    def test_vl_detectable_YES_vl_result_required(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
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
            'maternal_visit': self.maternal_visit,
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
