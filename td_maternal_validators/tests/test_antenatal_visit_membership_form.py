from django.test import TestCase
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow, relativedelta
from .models import TdConsentVersion, SubjectScreening, MaternalConsent
from ..form_validators import AntenatalVisitMembershipFormValidator


class TestAntenatalVisitMembershipForm(TestCase):

    def setUp(self):
        self.subjectscreening = SubjectScreening.objects.create(
            screening_identifier='ABC12345')
        self.td_consent_version = TdConsentVersion.objects.create(
            subjectscreening=self.subjectscreening, version='3',
            report_datetime=get_utcnow())
        self.td_consent_version_model = 'td_maternal_validators.tdconsentversion'
        AntenatalVisitMembershipFormValidator.consent_version_model =\
            self.td_consent_version_model
        self.subject_consent = MaternalConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')
        self.subject_consent_model = 'td_maternal_validators.maternalconsent'
        AntenatalVisitMembershipFormValidator.maternal_consent_model =\
            self.subject_consent_model

    def test_consentversion_object_does_not_exist(self):
        '''Tests if consent version object does not exist cleaned data
        validates or fails the tests if Validation Error is raised unexpectedly.'''

        self.td_consent_version.delete()
        cleaned_data = {
            'subjectscreening': self.subjectscreening}
        form_validator = AntenatalVisitMembershipFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_consent_version_object_exists(self):
        '''Tests if '''
        cleaned_data = {
            'subjectscreening': self.subjectscreening}
        form_validator = AntenatalVisitMembershipFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_maternal_consent_object_does_not_exist(self):
        '''Tests if maternal consent object does not exist cleaned data
        validates or fails the tests if Validation Error is raised unexpectedly.'''

        self.subject_consent.delete()
        cleaned_data = {
            'subjectscreening': self.subjectscreening
        }
        form_validator = AntenatalVisitMembershipFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_maternal_consent_object_exists(self):
        cleaned_data = {
            'subjectscreening': self.subjectscreening}
        form_validator = AntenatalVisitMembershipFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
