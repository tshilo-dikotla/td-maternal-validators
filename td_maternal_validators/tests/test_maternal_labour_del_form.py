from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, NO, POS
from .models import (MaternalArv, MaternalVisit,
                     MaternalConsent, Appointment, MaternalArvPreg,
                     RapidTestResult, AntenatalEnrollment)
from ..form_validators import MaternalLabDelFormValidator


@tag('lab_del')
class TestMaternalLabDelForm(TestCase):

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
        self.maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=YES, maternal_visit=self.maternal_visit)
        self.maternal_arv = MaternalArv.objects.create(
            maternal_arv_preg=self.maternal_arv_preg, start_date=get_utcnow().date())
        self.maternal_arv_model = 'td_maternal_validators.maternalarv'
        MaternalLabDelFormValidator.maternal_arv_model = self.maternal_arv_model
        self.rapid_test_result = RapidTestResult.objects.create(
            maternal_visit=self.maternal_visit, result=POS)
        self.rapid_test_result_model = 'td_maternal_validators.rapidtestresult'
        MaternalLabDelFormValidator.rapid_test_result_model = self.rapid_test_result_model
        self.enrollment_status = AntenatalEnrollment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            enrollment_hiv_status=POS)
        self.antenatal_enrollment_model = 'td_maternal_validators.antenatalenrollment'
        MaternalLabDelFormValidator.antenatal_enrollment_model =\
            self.antenatal_enrollment_model

    def test_arv_init_date_match_start_date(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'arv_initiation_date': get_utcnow().date(),
            'valid_regiment_duration': YES,
        }
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_arv_init_date_does_not_match_start_date(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'arv_initiation_date': (get_utcnow() - relativedelta(days=2)).date(),
            'valid_regiment_duration': YES, }
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('arv_initiation_date', form_validator._errors)

    def test_hiv_status_POS_valid_regiment_duration_invalid(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': NO,
            'arv_initiation_date': get_utcnow().date(), }
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('valid_regiment_duration', form_validator._errors)

    def test_hiv_status_POS_valid_regiment_duration_YES(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': YES,
            'arv_initiation_date': get_utcnow().date(), }
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_valid_regiment_duration_YES_arv_init_date_required(self):
        self.maternal_arv.delete()
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': YES,
            'arv_initiation_date': None}
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('arv_initiation_date', form_validator._errors)

    def test_valid_regiment_duration_YES_arv_init_date_provided(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': YES,
            'arv_initiation_date': get_utcnow().date()}
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
