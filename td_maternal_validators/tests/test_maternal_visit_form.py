from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES
from ..form_validators import MaternalVisitFormValidator
from td_maternal_validators.tests.models import (Appointment, SubjectScreening,
                                                 SubjectConsent,
                                                 TdConsentVersion)


@tag('mv')
class TestMaternalVisitFormValidator(TestCase):

    def setUp(self):
        self.subject_screening = SubjectScreening(
            screening_identifier='11111122',
            subject_identifier='11111111',
            report_datetime=get_utcnow(),
            has_omang=YES,
            age_in_years=21
        )
        self.subject_screening_model = \
            'td_maternal_validators.subjectscreening'
        self.maternal_consent_model = 'td_maternal_validators.subjectconsent'
        self.antenatal_enrollment_model = \
            'td_maternal_validators.antenatalenrollment'
        self.consent_version_model = 'td_maternal_validators.tdconsentversion'

        MaternalVisitFormValidator.maternal_consent_model = \
            self.maternal_consent_model
        MaternalVisitFormValidator.antenatal_enrollment_model = \
            self.antenatal_enrollment_model
        MaternalVisitFormValidator.consent_version_model = \
            self.consent_version_model
        MaternalVisitFormValidator.subject_screening_model = \
            self.subject_screening_model

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111122', screening_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')

        self.subject_screening = SubjectScreening.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            screening_identifier='11111111',
            age_in_years=22)

        self.td_consent_version = TdConsentVersion.objects.create(
            screening_identifier=self.subject_screening.screening_identifier,
            version='3', report_datetime=get_utcnow())

        self.appointment = Appointment.objects.create(
                subject_identifier=\
                self.subject_consent.subject_identifier,
                appt_datetime=get_utcnow(),
                visit_code='1000')
        self.options = {
            'report_datetime': get_utcnow(),
            'survival_status': 'unknown',
            'last_alive_date': None,
            'appointment': self.appointment
        }

    @tag('report')
    def test_report_datetime_not_before_consent(self):
        self.options['report_datetime'] = get_utcnow() - relativedelta(days=25)
        maternal_visit = MaternalVisitFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, maternal_visit.validate)

    def test_report_datetime_not_after_consent(self):
        self.options['report_datetime'] = get_utcnow()
        maternal_visit = MaternalVisitFormValidator(cleaned_data=self.options)
        maternal_visit.subject_screening_model = self.subject_screening_model
        maternal_visit.maternal_consent_model = self.maternal_consent_model
        maternal_visit.antenatal_enrollment_model = \
            self.antenatal_enrollment_model
        maternal_visit.consent_version_model = self.consent_version_model
        self.assertTrue(maternal_visit.validate)
        self.assertEqual({}, maternal_visit._errors)

    def test_last_alive_date_none(self):
        self.options['survival_status'] = 'alive'
        materna_visit = MaternalVisitFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, materna_visit.validate)

    def test_last_alive_date_not_none(self):
        self.options['survival_status'] = 'alive'
        self.options['last_alive_date'] = get_utcnow()
        maternal_visit = MaternalVisitFormValidator(cleaned_data=self.options)
        maternal_visit.subject_screening_model = self.subject_screening_model
        maternal_visit.maternal_consent_model = self.maternal_consent_model
        maternal_visit.antenatal_enrollment_model = \
            self.antenatal_enrollment_model
        maternal_visit.consent_version_model = self.consent_version_model
        self.assertTrue(maternal_visit.validate)
        self.assertEqual({}, maternal_visit._errors)
