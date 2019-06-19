from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from ..form_validators import MaternalArvPregFormValidator
from .models import MaternalVisit, Appointment, MaternalArvPreg
from .models import SubjectScreening, SubjectConsent, TdConsentVersion


@tag('map')
class TestMaternalArvPregForm(TestCase):

    def setUp(self):
        MaternalArvPregFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        MaternalArvPregFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        MaternalArvPregFormValidator.subject_screening_model = \
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

        self.td_consent_version = TdConsentVersion.objects.create(
            screening_identifier=self.subject_screening.screening_identifier,
            version='3', report_datetime=get_utcnow())

        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_consent.subject_identifier)

        self.maternal_arv_preg = MaternalArvPreg.objects.create(
            maternal_visit=self.maternal_visit)

    def test_medication_interrupted_invalid(self):
        '''Assert raises if arvs was interrupted but
        no reasons were given.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': YES,
            'interrupt': 'reason',
        }
        form_validator = MaternalArvPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_medication_interrupted_invalid_yes(self):
        '''Assert raises if arvs was interrupted but
        no reason was given.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': YES,
            'interrupt': NOT_APPLICABLE,
        }
        form_validator = MaternalArvPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('interrupt', form_validator._errors)

    @tag('mp2')
    def test_medication_interrupted_valid(self):
        '''True if arvs was not interrupted and no
        interrupt reason was provided.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': NO,
            'interrupt': NOT_APPLICABLE,
            'report_datetime': get_utcnow()
        }
        form_validator = MaternalArvPregFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised. Got {e}')

    def test_medication_interrupted_invalid_none(self):
        '''Assert raises if no interruptions but
        reason is given.
        '''
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_interrupt': NO,
            'interrupt': 'reason',
        }
        form_validator = MaternalArvPregFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('interrupt', form_validator._errors)
