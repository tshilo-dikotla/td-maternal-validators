from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, NEG, NOT_APPLICABLE, MALE, YES, NO
from .models import (
    MaternalConsent, Appointment, MaternalVisit, RapidTestResult, AntenatalEnrollment,
    RegisteredSubject, ListModel)
from ..form_validators import MaternalMedicalHistoryFormValidator


class TestMaternalMedicalHistoryForm(TestCase):
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
        self.rapid_test_result = RapidTestResult.objects.create(
            maternal_visit=self.maternal_visit, result=NEG)
        self.registered_subject = RegisteredSubject.objects.create(
            first_name='First_Name', last_name='Last_Name', gender=MALE)
        self.rapid_test_result_model = 'td_maternal_validators.rapidtestresult'
        MaternalMedicalHistoryFormValidator.rapid_test_result_model = \
            self.rapid_test_result_model
        self.enrollment_status = AntenatalEnrollment.objects.create(
            registered_subject=self.registered_subject, enrollment_hiv_status=POS)
        self.antenatal_enrollment_model = 'td_maternal_validators.antenatalenrollment'
        MaternalMedicalHistoryFormValidator.antenatal_enrollment_model = \
            self.antenatal_enrollment_model

    def test_subject_status_neg(self):
        '''True if chronic_since is yes and who_diagnosis is no.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': YES,
            'who_diagnosis': NO,
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_neg_valid(self):
        '''True if chronic_since is no and who_diagnosis is Not_applicable.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': NO,
            'who_diagnoses': NOT_APPLICABLE,
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_neg_invalid(self):
        '''Assert raises exception if chronic_since is none but who_diagnosis is yes.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': None,
            'who_diagnosis': YES,
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_neg_na_valid(self):
        '''True if chronic_since is none and who_diagnosis is Not_applicable.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': None,
            'who_diagnosis': NOT_APPLICABLE,
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_pos_valid(self):
        '''True if chronic_since is none and who_diagnosis is Not_applicable.
        '''
        self.rapid_test_result.result = POS
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': None,
            'who_diagnosis': NOT_APPLICABLE,
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_pos_invalid(self):
        '''Assert raises exception if the result is positive and who_diagnosis is none.
        '''
        self.rapid_test_result.result = POS
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': YES,
            'who_diagnosis': None,
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_pos_no_valid(self):
        '''True if chronic_since is none and who_diagnosis is Not_applicable.
        '''
        self.rapid_test_result.result = POS
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': NO,
            'who_diagnosis': NOT_APPLICABLE,
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_pos_yes_who_none(self):
        '''Assert raises exception if who is none and'
        'who_diagnosis is not_applicable.
        '''
        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': YES,
            'who_diagnosis': NOT_APPLICABLE,
            'who': None
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_pos_yes_who_na(self):
        '''Assert raises exception if who has no list and'
        'who_diagnosis is not_applicable.
        '''
        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': YES,
            'who_diagnosis': NOT_APPLICABLE,
            'who': NOT_APPLICABLE
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_pos_yes_who_valid(self):
        '''Assert raises exception if who has a list and'
        'who_diagnosis is not_applicable.
        '''
        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        ListModel.objects.create(name='who', short_name='who')
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': YES,
            'who_diagnosis': NOT_APPLICABLE,
            'who': ListModel.objects.all()
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_pos_yes_who_list_yes(self):
        '''True if who has a list and who_diagnosis is yes.
        '''
        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        ListModel.objects.create(name='who', short_name='who')
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'chronic_since': YES,
            'who_diagnosis': YES,
            'who': ListModel.objects.all()
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_if_mother_medication_true(self):
        '''True if mother_medication is selected
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'mother_medication': True,
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_positive_mother_seropositive_yes(self):
        '''True if sero_posetive is yes and perinataly_infected, know_hiv_status,
        lowest_cd4_known are given
        '''
        cleaned_data = {
            'sero_posetive': YES,
            'perinataly_infected': YES,
            'know_hiv_status': YES,
            'lowest_cd4_known': YES
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_positive_mother_seropositive_no(self):
        '''True if sero_posetive is yes and perinataly_infected, know_hiv_status,
        lowest_cd4_known are given
        '''
        cleaned_data = {
            'sero_posetive': NO,
            'perinataly_infected': NOT_APPLICABLE,
            'know_hiv_status': NOT_APPLICABLE,
            'lowest_cd4_known': NOT_APPLICABLE
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_negative_mother_seropositive_no_cd4_not(self):
        '''True if sero_posetive is yes and perinataly_infected, know_hiv_status,
        lowest_cd4_known are given
        '''
        cleaned_data = {
            'sero_posetive': NO,
            'cd4_date': None,
            'cd4_count': None,
            'is_date_estimated': None,
            'lowest_cd4_known': NOT_APPLICABLE
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_negative_no_cd4_not(self):
        '''True if sero_posetive is yes and perinataly_infected, know_hiv_status,
        lowest_cd4_known are given
        '''
        cleaned_data = {
            'sero_posetive': YES,
            'cd4_date': get_utcnow().date() + relativedelta(years=1),
            'cd4_count': 20,
            'is_date_estimated': get_utcnow().date() + relativedelta(years=2),
            'lowest_cd4_known': NOT_APPLICABLE
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_negative_no_cd4_invalid(self):
        '''True if sero_posetive is yes and perinataly_infected, know_hiv_status,
        lowest_cd4_known are given
        '''
        cleaned_data = {
            'sero_posetive': NO,
            'cd4_date': None,
            'cd4_count': None,
            'is_date_estimated': None,
            'lowest_cd4_known': NOT_APPLICABLE
        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def validate_haart_start_date(self):
        '''True if haart_start_date is after the hiv_diagnosis date.
        '''
        cleaned_data = {
            'haart_start_date': get_utcnow().date(),
            'date_hiv_diagnosis': get_utcnow().date() + relativedelta(days=10),

        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def validate_haart_start_date_invalid(self):
        '''Assert raises exception if the haart_satrt_date is greater than'
        'the date_hiv_diagnosis.
        '''
        cleaned_data = {
            'haart_start_date': get_utcnow().date() + relativedelta(days=10),
            'date_hiv_diagnosis': get_utcnow().date(),

        }
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('date_hiv_diagnosis', form_validator._errors)
