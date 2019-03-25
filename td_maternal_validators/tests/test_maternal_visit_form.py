from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import OFF_STUDY, ON_STUDY
from edc_constants.constants import UNKNOWN, DEAD, ALIVE

from td_maternal_validators.tests.models import (Appointment, SubjectScreening,
                                                 SubjectConsent,
                                                 TdConsentVersion)

from ..form_validators import MaternalVisitFormValidator


@tag('mv')
class TestMaternalVisitFormValidator(TestCase):

    def setUp(self):
        MaternalVisitFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        MaternalVisitFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        MaternalVisitFormValidator.subject_screening_model = \
            'td_maternal_validators.subjectscreening'
        MaternalVisitFormValidator.antenatal_enrollment_model = \
            'td_maternal_validators.antenatalenrollment'

        self.subject_identifier = '11111111'
        self.subject_screening = SubjectScreening.objects.create(
            subject_identifier=self.subject_identifier,
            screening_identifier='ABC12345',
            age_in_years=22)

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier=self.subject_identifier, screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')

        self.td_consent_version = TdConsentVersion.objects.create(
            screening_identifier=self.subject_screening.screening_identifier,
            version='3', report_datetime=get_utcnow())

        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

    def test_consent_invalid(self):
        self.subject_consent = None
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': DEAD,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('study_status', form_validator._errors)

    def test_last_alive_date_not_required_valid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': UNKNOWN,
            'last_alive_date': None,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_death_study_status_invalid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': DEAD,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('study_status', form_validator._errors)

    def test_death_study_status_valid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': DEAD,
            'last_alive_date': get_utcnow().date(),
            'study_status': OFF_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
