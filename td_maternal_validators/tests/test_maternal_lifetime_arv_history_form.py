from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import (
    RESTARTED, NO, YES, CONTINUOUS, STOPPED, NOT_APPLICABLE, NEG, POS)

from ..form_validators import MaternalLifetimeArvHistoryFormValidator
from .models import AntenatalEnrollment, MaternalObstericalHistory
from .models import MaternalMedicalHistory
from .models import SubjectConsent, Appointment, MaternalVisit


class TestMaternalLifetimeArvHistoryForm(TestCase):

    def setUp(self):
        MaternalLifetimeArvHistoryFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'

        MaternalLifetimeArvHistoryFormValidator.medical_history_model = \
            'td_maternal_validators.maternalmedicalhistory'

        MaternalLifetimeArvHistoryFormValidator.antenatal_enrollment_model = \
            'td_maternal_validators.antenatalenrollment'

        MaternalLifetimeArvHistoryFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'

        MaternalLifetimeArvHistoryFormValidator.ob_history_model = \
            'td_maternal_validators.maternalobstericalhistory'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow())

        self.antenatal_enrollment = AntenatalEnrollment.objects.create(
            subject_identifier='11111111',
            enrollment_hiv_status=NEG, week32_result=POS,
            rapid_test_result=POS, rapid_test_date=get_utcnow().date(),
            week32_test_date=get_utcnow().date())

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,)

        self.medical_history = MaternalMedicalHistory.objects.create(
            maternal_visit=self.maternal_visit,
            date_hiv_diagnosis=get_utcnow().date())

        self.ob_history = MaternalObstericalHistory.objects.create(
            maternal_visit=self.maternal_visit, prev_pregnancies=5)

    def test_preg_on_haart_no_preg_prior_invalid(self):
        '''Asserts raises exception if subject was not on triple
        antiretrovirals at the time she became pregnant but prior to
        pregnancy value is restarted.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'preg_on_haart': NO,
            'prior_preg': RESTARTED, }
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)

    def test_preg_on_haart_no_preg_prior_invalid2(self):
        '''Asserts raises exception if subject was not on triple
        antiretrovirals at the time she became pregnant but prior to
        pregnancy value is continuous.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'preg_on_haart': NO,
            'prior_preg': CONTINUOUS}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)

    def test_preg_on_haart_yes_preg_prior_invalid(self):
        '''Asserts raises exception if subject was still on triple
        antiretrovirals at the time she became pregnant but prior to
        pregnancy value is stopped.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'maternal_visit': self.maternal_visit,
            'preg_on_haart': YES,
            'prior_preg': STOPPED,
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': 'yes',
            'report_datetime': get_utcnow() + relativedelta(days=30)}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)

    def test_antenatal_enrollment_hiv_test_date_provided(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_preg_haart': YES,
            'haart_start_date': get_utcnow().date() - relativedelta(days=30),
            'is_date_estimated': 'no',
            'report_datetime': get_utcnow() + relativedelta(days=30)}

        self.antenatal_enrollment.week32_test_date = get_utcnow().date()
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_medical_history_diagnosis_date_provided(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_preg_haart': YES,
            'haart_start_date': get_utcnow().date() - relativedelta(days=30),
            'is_date_estimated': 'no',
            'report_datetime': get_utcnow()}

        self.medical_history.date_hiv_diagnosis = get_utcnow().date()
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_prev_preg_haart_yes_start_date_provided(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_preg_haart': YES,
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': 'no',
            'report_datetime': get_utcnow()}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_haart_start_date_valid_date_est_provided(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': 'yes',
            'report_datetime': get_utcnow() + relativedelta(days=30)}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_haart_start_date_invalid_date_est_valid(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'haart_start_date': None,
            'is_date_estimated': None}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_consent_date_less_than_report_date_valid(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        self.subject_consent.consent_datetime = \
            get_utcnow() - relativedelta(days=30)
        self.subject_consent.save()

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': NO,
            'maternal_visit': self.maternal_visit,
            'report_datetime': get_utcnow()}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_consent_date_more_than_report_date_invalid(self):
        '''Asserts raises exception if subject received antiretrovirals during
        a prior pregnancy and date first started given but does not state if
        the date is estimated or not.'''

        self.maternal_visit.report_datetime = get_utcnow() - relativedelta(days=30)
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': NO,
            'maternal_visit': self.maternal_visit,
            'report_datetime': get_utcnow() - relativedelta(days=30)}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('report_datetime', form_validator._errors)

    def test_haart_start_less_than_dob_invalid(self):
        '''Asserts raises exception if antiretrovirals date first started given
        is less than subject's date of birth.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'haart_start_date': get_utcnow().date() - relativedelta(years=30),
            'is_date_estimated': NO,
            'maternal_visit': self.maternal_visit,
            'report_datetime': get_utcnow()}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('haart_start_date', form_validator._errors)

    def test_haart_start_more_than_dob_valid(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'haart_start_date': get_utcnow().date(),
            'is_date_estimated': NO,
            'maternal_visit': self.maternal_visit,
            'report_datetime': get_utcnow()}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ob_prev_preg_zero_prev_preg_azt_na(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        self.ob_history.prev_pregnancies = 0
        self.ob_history.save()

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_preg_azt': NOT_APPLICABLE}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ob_prev_preg_zero_prev_preg_azt_invalid(self):
        '''Asserts raises exception if subject obsterical previous pregnancies
        is 0 and AZT monotherapy in a previous pregnancy is given.'''

        self.ob_history.prev_pregnancies = 0
        self.ob_history.save()

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_preg_azt': YES}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prev_preg_azt', form_validator._errors)

    def test_ob_prev_zero_prev_sdnvp_labour_na(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        self.ob_history.prev_pregnancies = 0
        self.ob_history.save()

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_sdnvp_labour': NOT_APPLICABLE}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ob_prev_zero_prev_sdnvp_labour_invalid(self):
        '''Asserts raises exception if subject obsterical previous pregnancies
        is 0 and single-dose NVP in a previous pregnancy is given.'''

        self.ob_history.prev_pregnancies = 0
        self.ob_history.save()

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_sdnvp_labour': YES}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prev_sdnvp_labour', form_validator._errors)

    def test_ob_prev_zero_prev_preg_haart_na(self):
        '''Tests validates cleaned data given or fails the tests if validation
        error raised unexpectedly.'''

        self.ob_history.prev_pregnancies = 0
        self.ob_history.save()

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_preg_haart': NOT_APPLICABLE}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ob_prev_zero_prev_preg_haart_invalid(self):
        '''Asserts raises exception if subject obsterical previous pregnancies
        is 0 and triple antiretrovirals during a prior pregnancy is given.'''

        self.ob_history.prev_pregnancies = 0
        self.ob_history.save()

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'prev_preg_haart': NO}
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prev_preg_haart', form_validator._errors)

    def test_ob_prev_not_exist(self):
        '''Asserts raises exception if the maternal obsterical history model
        object does not exist'''
        self.ob_history.delete()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
        }
        form_validator = MaternalLifetimeArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
