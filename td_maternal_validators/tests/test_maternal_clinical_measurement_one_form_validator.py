from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow

from ..form_validators import MaternalClinicalMeasurememtsOneFormValidator
from .models import MaternalVisit, Appointment
from .models import SubjectScreening, SubjectConsent


class TestMaternalClinicalTestOneForm(TestCase):

    def setUp(self):
        MaternalClinicalMeasurememtsOneFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        MaternalClinicalMeasurememtsOneFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        MaternalClinicalMeasurememtsOneFormValidator.subject_screening_model = \
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

    def test_systolic_bp_yes_valid(self):
        '''True if systolic_bp is selected
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'systolic_bp': 30,
            'diastolic_bp': 20,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diastolic_bp_yes_valid(self):
        '''True if diastolic_bp is selected
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'systolic_bp': 50,
            'diastolic_bp': 40,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_systolic_bp_less_invalid(self):
        '''Assert raises exception if systolic_bp
        is < diastolic_bp.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'systolic_bp': 20,
            'diastolic_bp': 40,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diastolic_bp', form_validator._errors)

    def test_systolic_bp_greater_valid(self):
        '''True if diastolic_bp is selected
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'systolic_bp': 50,
            'diastolic_bp': 40,
        }
        form_validator = MaternalClinicalMeasurememtsOneFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
