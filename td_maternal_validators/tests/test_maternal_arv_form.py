from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import MaternalArvFormValidator
from .models import (MaternalArvPreg, MaternalArv,
                     MaternalLifetimeArvHistory, SubjectConsent,
                     MaternalVisit, Appointment)


class TestMaternalArvForm(TestCase):

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111', consent_datetime=get_utcnow(),
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment)
        arv_history_model = 'td_maternal_validators.maternallifetimearvhistory'
        MaternalArvFormValidator.arv_history_model = arv_history_model

    def test_stop_date_invalid(self):
        '''Assert Raises if start_date is > stop_date.
        '''
        cleaned_data = {
            "stop_date": get_utcnow().date(),
            "start_date": get_utcnow().date() + timedelta(days=30),
        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('stop_date', form_validator._errors)

    def test_stop_date_valid(self):
        '''True if start_date < stop_date.
        '''
        MaternalLifetimeArvHistory.objects.create(
            haart_start_date=get_utcnow().date() + timedelta(days=30),
            maternal_visit=self.maternal_visit)
        maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=YES, maternal_visit=self.maternal_visit)
        MaternalArv.objects.create(maternal_arv_preg=maternal_arv_preg)

        cleaned_data = {
            "maternal_arv_preg": maternal_arv_preg,
            "start_date": get_utcnow().date() + timedelta(days=30),
            "stop_date": get_utcnow().date() + timedelta(days=30),
            "reason_for_stop": 'reason',
            "arv_code": 'Value',

        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_stop_date_equals_invalid(self):
        '''Invalid if the stop_date < start_date.
        '''
        MaternalLifetimeArvHistory.objects.create(
            haart_start_date=get_utcnow().date() + timedelta(days=30),
            maternal_visit=self.maternal_visit)
        maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=YES, maternal_visit=self.maternal_visit)
        MaternalArv.objects.create(maternal_arv_preg=maternal_arv_preg)

        cleaned_data = {
            "maternal_arv_preg": maternal_arv_preg,
            "stop_date": get_utcnow().date() + timedelta(days=33),
            "start_date": get_utcnow().date() + timedelta(days=30),
            "reason_for_stop": 'reason',
            "arv_code": 'Value',
        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_took_marternal_arv_yes_valid(self):
        '''True if subject took maternal arv and provides the arv_code
        '''
        MaternalLifetimeArvHistory.objects.create(
            haart_start_date=get_utcnow().date() + timedelta(days=30),
            maternal_visit=self.maternal_visit)
        maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=YES, maternal_visit=self.maternal_visit)
        MaternalArv.objects.create(maternal_arv_preg=maternal_arv_preg)

        cleaned_data = {
            "maternal_arv_preg": maternal_arv_preg,
            "start_date": get_utcnow().date() + timedelta(days=31),
            "stop_date": get_utcnow().date() + timedelta(days=32),
            "reason_for_stop": 'reason',
            "arv_code": 'Value',
        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_took_maternal_arv_yes_invalid(self):
        '''Assert raises exception if the took_arv is yes but arv_code is not given
        '''
        maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=YES, maternal_visit=self.maternal_visit)
        MaternalArv.objects.create(maternal_arv_preg=maternal_arv_preg)

        cleaned_data = {
            "maternal_arv_preg": maternal_arv_preg,
            "stop_date": get_utcnow().date(),
            "start_date": get_utcnow().date(),
            "arv_code": None,
        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('arv_code', form_validator._errors)

    def test_took_maternal_arv_no_valid(self):
        '''True if took_arv is no and arv_code is none
        '''
        MaternalLifetimeArvHistory.objects.create(
            haart_start_date=get_utcnow().date() + timedelta(days=30),
            maternal_visit=self.maternal_visit)
        maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=NO, maternal_visit=self.maternal_visit)
        MaternalArv.objects.create(maternal_arv_preg=maternal_arv_preg)

        cleaned_data = {
            "maternal_arv_preg": maternal_arv_preg,
            "start_date": get_utcnow().date() + timedelta(days=31),
            "stop_date": get_utcnow().date() + timedelta(days=32),
            "reason_for_stop": 'reason',
            "arv_code": None,
        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_historical_arv_date_invalid(self):
        '''Assert raises exception if start date is less than arv_history.
        '''

        MaternalLifetimeArvHistory.objects.create(
            haart_start_date=get_utcnow().date() + timedelta(days=30),
            maternal_visit=self.maternal_visit)
        maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=NO, maternal_visit=self.maternal_visit)

        cleaned_data = {
            "maternal_arv_preg": maternal_arv_preg,
            "arv_history": MaternalLifetimeArvHistory.objects.get(
                maternal_visit=maternal_arv_preg.maternal_visit),
            "start_date": get_utcnow().date(),
            "stop_date": get_utcnow().date()
        }
        form_validator = MaternalArvFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('start_date', form_validator._errors)

    def test_historical_arv_date_valid(self):
        '''True if the start date is greater than the arv_history.
        '''

        MaternalLifetimeArvHistory.objects.create(
            haart_start_date=get_utcnow().date(),
            maternal_visit=self.maternal_visit)
        maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=NO, maternal_visit=self.maternal_visit)

        cleaned_data = {
            "maternal_arv_preg": maternal_arv_preg,
            "arv_history": MaternalLifetimeArvHistory.objects.get(
                maternal_visit=maternal_arv_preg.maternal_visit),
            "start_date": get_utcnow().date(),
            "stop_date": get_utcnow().date() + timedelta(days=30),
            "reason_for_stop": 'reason'
        }
        form_validator = MaternalArvFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_arv_stopped_valid(self):
        '''True if the stop_date is specified and the reason_for_stop is given.
        '''
        MaternalLifetimeArvHistory.objects.create(
            haart_start_date=get_utcnow().date() + timedelta(days=30),
            maternal_visit=self.maternal_visit)
        maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=NO, maternal_visit=self.maternal_visit)

        cleaned_data = {
            "maternal_arv_preg": maternal_arv_preg,
            "arv_history": MaternalLifetimeArvHistory.objects.get(
                maternal_visit=maternal_arv_preg.maternal_visit),
            "stop_date": get_utcnow().date() + timedelta(days=30),
            "start_date": get_utcnow().date() + timedelta(days=30),
            "reason_for_stop": 'reason'
        }
        form_validator = MaternalArvFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_arv_stopped_invalid(self):
        '''Assert raises exception if stop_date is specified but the reason is none.
        '''
        MaternalLifetimeArvHistory.objects.create(
            haart_start_date=get_utcnow().date() + timedelta(days=30),
            maternal_visit=self.maternal_visit)
        maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=NO, maternal_visit=self.maternal_visit)

        cleaned_data = {
            "maternal_arv_preg": maternal_arv_preg,
            "arv_history": MaternalLifetimeArvHistory.objects.get(
                maternal_visit=maternal_arv_preg.maternal_visit),
            "start_date": get_utcnow().date() + timedelta(days=30),
            "stop_date": get_utcnow().date() + timedelta(days=30),
            "reason_for_stop": None
        }
        form_validator = MaternalArvFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_for_stop', form_validator._errors)
