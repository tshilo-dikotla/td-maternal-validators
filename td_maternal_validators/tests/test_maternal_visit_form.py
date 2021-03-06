from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import OFF_STUDY, ON_STUDY
from edc_constants.constants import UNKNOWN, DEAD, ALIVE, YES, PARTICIPANT, NO
from edc_visit_tracking.constants import LOST_VISIT
from td_maternal_validators.tests.models import (TdConsentVersion,
                                                 KaraboSubjectScreening,
                                                 KaraboSubjectConsent)
from td_maternal_validators.tests.models import Appointment, SubjectScreening
from td_maternal_validators.tests.models import SubjectConsent, MaternalLabourDel

from ..form_validators import MaternalVisitFormValidator


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
        MaternalVisitFormValidator.maternal_labour_del_model = \
            'td_maternal_validators.maternallabourdel'
        MaternalVisitFormValidator.karabo_subject_screening_model = \
            'td_maternal_validators.karabosubjectscreening'
        MaternalVisitFormValidator.karabo_subject_consent_model = \
            'td_maternal_validators.karabosubjectconsent'

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
            visit_code='1000M')

        self.appointment1 = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1010M')

        self.appointment2 = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1020M')

        self.appointment3 = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000M')

    def test_study_covid_visit_valid(self):

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment,
            'covid_visit': YES,
            'is_present': NO
        }

        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_study_covid_visit_invalid(self):

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment,
            'covid_visit': YES,
            'is_present': YES
        }

        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_present', form_validator._errors)

    def test_study_status_on_dead_valid(self):

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }

        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

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

    def test_unknown_study_status_invalid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': UNKNOWN,
            'last_alive_date': get_utcnow().date(),
            'study_status': OFF_STUDY,
            'info_source': PARTICIPANT,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('survival_status', form_validator._errors)

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': UNKNOWN,
            'last_alive_date': get_utcnow().date(),
            'study_status': OFF_STUDY,
            'info_source': 'blahblah',
            'is_present': YES,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('survival_status', form_validator._errors)

    def test_unknown_study_status_valid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': DEAD,
            'last_alive_date': get_utcnow().date(),
            'study_status': OFF_STUDY,
            'info_source': 'blahblah',
            'is_present': NO,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_reason_offstudy_invalid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'reason': LOST_VISIT,
            'is_present': YES,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('study_status', form_validator._errors)

    def test_reason_offstudy_valid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'reason': LOST_VISIT,
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

    def test_is_presnt_info_source_invalid(self):
        self.subject_consent = None
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'is_present': YES,
            'info_source': 'blahblah',
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('info_source', form_validator._errors)

    def test_is_presnt_info_source_valid(self):
        self.subject_consent = None
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'is_present': YES,
            'info_source': PARTICIPANT,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_karabo_screening_invalid(self):
        MaternalLabourDel.objects.create(
            subject_identifier=self.appointment.subject_identifier,
            delivery_datetime=get_utcnow() - relativedelta(months=18))
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('__all__', form_validator._errors)

    def test_karabo_screening_ineligile(self):
        MaternalLabourDel.objects.create(
            subject_identifier=self.appointment.subject_identifier,
            delivery_datetime=get_utcnow() - relativedelta(months=18))

        KaraboSubjectScreening.objects.create(
            subject_identifier=self.appointment.subject_identifier,
            is_eligible=False)

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_karabo_consent_invalid(self):
        MaternalLabourDel.objects.create(
            subject_identifier=self.appointment.subject_identifier,
            delivery_datetime=get_utcnow() - relativedelta(months=18))

        KaraboSubjectScreening.objects.create(
            subject_identifier=self.appointment.subject_identifier,
            is_eligible=True)

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('__all__', form_validator._errors)

    def test_karabo_screening_valid(self):

        KaraboSubjectScreening.objects.create(
            subject_identifier=self.appointment.subject_identifier,
            is_eligible=True)

        KaraboSubjectConsent.objects.create(
            subject_identifier=self.appointment.subject_identifier,
            consent_datetime=get_utcnow())

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
