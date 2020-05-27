from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES

from ..form_validators import MaternalFoodSecurityFormValidator
from .models import SubjectConsent, MaternalVisit, Appointment


@tag('fs')
class TestMaternalFoodSecurityForm(TestCase):

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow())

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())

    def test_skip_meals_frequency_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'skip_meals': YES,
            'skip_meals_frequency': 'blah'
        }
        form_validator = MaternalFoodSecurityFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_skip_meals_frequency_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'skip_meals': YES,
            'skip_meals_frequency': None
        }
        form_validator = MaternalFoodSecurityFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('skip_meals_frequency', form_validator._errors)
