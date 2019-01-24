from dateutil.relativedelta import relativedelta
from django.forms import forms
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, NOT_APPLICABLE

from ..constants import NEVER_STARTED
from ..form_validators import MarternalArvPostFormValidator
from .models import (Appointment, MaternalVisit, MaternalConsent,
                     MaternalArvPostAdh)
from django.core.exceptions import ValidationError


class MaternalArvPostFormValidator(TestCase):

    def setUp(self):
        self.subject_consent = MaternalConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment)
        self.maternalarvpost = MaternalArvPostAdh.objects.create(
            maternal_visit=self.maternal_visit)
        maternal_arv_post_adh = 'td_maternal_validators.maternalarvpostadh'
        MarternalArvPostFormValidator.maternal_arv_post_adh = maternal_arv_post_adh

    def test_arv_status_no_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'on_arv_since': NO,
            'arv_status': NEVER_STARTED}
        form_validator = MarternalArvPostFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)

    def test_on_arv_since_no_reason_na_valid(self):
        self.maternalarvpost.delete()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'on_arv_since': NO,
            'on_arv_reason': NOT_APPLICABLE}
        form_validator = MarternalArvPostFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unexpectedly. Got{e}')

    def test_on_arv_since_no_reason_given_invalid(self):
        self.maternalarvpost.delete()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'on_arv_since': NO,
            'on_arv_reason': 'some reason'}
        form_validator = MarternalArvPostFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('on_arv_reason', form_validator._errors)
