from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, NO, POS, NEG, NOT_APPLICABLE

from ..form_validators import MaternalLabDelFormValidator
from .models import (MaternalArv, MaternalVisit,
                     SubjectConsent, Appointment, MaternalArvPreg,
                     SubjectScreening, TdConsentVersion)


class MaternalStatusHelper:

    def __init__(self, status=None):
        self.status = status

    @property
    def hiv_status(self):
        return self.status


class TestMaternalLabDelForm(TestCase):

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')

        subject_consent_model = 'td_maternal_validators.subjectconsent'
        MaternalLabDelFormValidator.maternal_consent_model =\
            subject_consent_model

        self.subjectscreening = SubjectScreening.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            screening_identifier='ABC12345', age_in_years=22)
        subject_screening_model = 'td_maternal_validators.subjectscreening'
        MaternalLabDelFormValidator.subject_screening_model =\
            subject_screening_model

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier)
        maternal_visit_model = 'td_maternal_validators.maternalvisit'
        MaternalLabDelFormValidator.maternal_visit_model =\
            maternal_visit_model

        self.maternal_arv_preg = MaternalArvPreg.objects.create(
            took_arv=YES, maternal_visit=maternal_visit)
        self.maternal_arv = MaternalArv.objects.create(
            maternal_arv_preg=self.maternal_arv_preg, start_date=get_utcnow().date())
        maternal_arv_model = 'td_maternal_validators.maternalarv'
        MaternalLabDelFormValidator.maternal_arv_model = maternal_arv_model

        self.td_consent_version = TdConsentVersion.objects.create(
            screening_identifier=self.subjectscreening.screening_identifier,
            version='3', report_datetime=get_utcnow())
        td_consent_version_model = 'td_maternal_validators.tdconsentversion'
        MaternalLabDelFormValidator.consent_version_model =\
            td_consent_version_model

    def test_arv_init_date_match_start_date(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'arv_initiation_date': get_utcnow().date(),
            'delivery_datetime': get_utcnow() + relativedelta(weeks=5),
            'valid_regiment_duration': YES,
        }
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_arv_init_date_does_not_match_start_date(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'arv_initiation_date': (get_utcnow() - relativedelta(days=2)).date(),
            'delivery_datetime': get_utcnow() + relativedelta(weeks=5),
            'valid_regiment_duration': YES, }
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('arv_initiation_date', form_validator._errors)

    def test_hiv_status_POS_valid_regiment_duration_invalid(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': NO,
            'delivery_datetime': get_utcnow(),
            'arv_initiation_date': get_utcnow().date(), }
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('valid_regiment_duration', form_validator._errors)

    def test_hiv_status_POS_valid_regiment_duration_YES(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': YES,
            'delivery_datetime': get_utcnow() + relativedelta(weeks=5),
            'arv_initiation_date': get_utcnow().date(), }
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
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
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('arv_initiation_date', form_validator._errors)

    def test_valid_regiment_duration_YES_arv_init_date_provided(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': YES,
            'arv_initiation_date': get_utcnow().date(),
            'delivery_datetime': get_utcnow() + relativedelta(weeks=5)}
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_delivery_date_within_4wks_arv_init_date_invalid(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': YES,
            'arv_initiation_date': get_utcnow().date(),
            'delivery_datetime': get_utcnow() + relativedelta(weeks=2)}
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('delivery_datetime', form_validator._errors)

    def test_delivery_date_more_than_4wks_arv_init_date_valid(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': YES,
            'arv_initiation_date': get_utcnow().date(),
            'delivery_datetime': get_utcnow() + relativedelta(weeks=5)}
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hiv_status_NEG_valid_regiment_duration_NO_invalid(self):
        self.maternal_arv.delete()
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': NO, }
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('valid_regiment_duration', form_validator._errors)

    def test_hiv_status_NEG_valid_regiment_duration_YES_invalid(self):
        self.maternal_arv.delete()
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': YES, }
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('valid_regiment_duration', form_validator._errors)

    def test_hiv_status_NEG_valid_regiment_duration_NA_valid(self):
        self.maternal_arv.delete()
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': NOT_APPLICABLE, }
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hiv_status_NEG_arv_init_date_invalid(self):
        self.maternal_arv.delete()
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': NOT_APPLICABLE,
            'arv_initiation_date': get_utcnow().date()
        }
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('arv_initiation_date', form_validator._errors)

    def test_hiv_status_NEG_arv_init_date_valid(self):
        self.maternal_arv.delete()
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'valid_regiment_duration': NOT_APPLICABLE,
            'arv_initiation_date': None
        }
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalLabDelFormValidator.maternal_status_helper = maternal_status
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_still_births_zero_live_births_one_valid(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'arv_initiation_date': get_utcnow().date(),
            'valid_regiment_duration': YES,
            'delivery_datetime': get_utcnow() + relativedelta(weeks=5),
            'still_births': 0,
            'live_infants_to_register': 1
        }
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_still_births_one_live_births_zero_valid(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'arv_initiation_date': get_utcnow().date(),
            'valid_regiment_duration': YES,
            'delivery_datetime': get_utcnow() + relativedelta(weeks=5),
            'still_births': 1,
            'live_infants_to_register': 0
        }
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_live_births_one_still_births_invalid(self):
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier,
            'arv_initiation_date': get_utcnow().date(),
            'valid_regiment_duration': YES,
            'delivery_datetime': get_utcnow() + relativedelta(weeks=5),
            'still_births': 1,
            'live_infants_to_register': 1
        }
        form_validator = MaternalLabDelFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('still_births', form_validator._errors)
