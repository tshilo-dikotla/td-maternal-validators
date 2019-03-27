from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, POS, NEG, IND, NO

from ..form_validators import RapidTestResultFormValidator
from .models import MaternalVisit
from .models import SubjectConsent, AntenatalEnrollment, Appointment


class TestRapidTestResultForm(TestCase):

    def setUp(self):
        RapidTestResultFormValidator.antenatal_enrollment_model = \
            'td_maternal_validators.antenatalenrollment'

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
            subject_identifier=self.subject_consent.subject_identifier,)

        self.antenatal_enrollment = AntenatalEnrollment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            week32_test=NEG,
            enrollment_hiv_status=NEG,
            week32_result=NEG,
            rapid_test_done=YES,
            rapid_test_result=NEG,
            rapid_test_date=get_utcnow().date(),
            report_datetime=get_utcnow())

    def test_rapid_test_done_YES_result_date_required(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': YES,
            'result_date': None,
            'result': POS or NEG or IND}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('result_date', form_validator._errors)

    def test_rapid_test_done_YES_result_date_provided(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': YES,
            'result_date': get_utcnow().date(),
            'result': POS or NEG or IND}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_rapid_test_done_YES_result_required(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': YES,
            'result_date': get_utcnow().date(),
            'result': None}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('result', form_validator._errors)

    def test_rapid_test_done_YES_result_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': YES,
            'result_date': get_utcnow().date(),
            'result': POS or NEG or IND}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_rapid_test_done_NO_result_date_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': NO,
            'result_date': get_utcnow().date()}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('result_date', form_validator._errors)

    def test_rapid_test_done_NO_result_date_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': NO,
            'result_date': None}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_rapid_test_done_NO_result_invalid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': NO,
            'result': POS or NEG or IND}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('result', form_validator._errors)

    def test_rapid_test_done_NO_result_valid(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': NO,
            'result': None}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_antenatal_enrollement_rapid_test(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'rapid_test_done': YES,
            'result_date': (get_utcnow() - relativedelta(months=4)).date(),
            'result': NEG}
        form_validator = RapidTestResultFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
