from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta

from ..form_validators import AntenatalVisitMembershipFormValidator
from .models import TdConsentVersion, SubjectScreening, MaternalConsent


class TestAntenatalVisitMembershipForm(TestCase):

    def setUp(self):
        self.screening_identifier = 'ABC12345'
        self.subject_consent = MaternalConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')
        self.subject_consent_model = 'td_maternal_validators.maternalconsent'
        AntenatalVisitMembershipFormValidator.maternal_consent_model =\
            self.subject_consent_model
        self.subject_screening = SubjectScreening.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            screening_identifier=self.screening_identifier,
            age_in_years=22)
        self.subject_screening_model = 'td_maternal_validators.subjectscreening'
        AntenatalVisitMembershipFormValidator.subject_screening_model =\
            self.subject_screening_model
        self.td_consent_version = TdConsentVersion.objects.create(
            subject_screening=self.subject_screening, version='3',
            report_datetime=get_utcnow())
        self.td_consent_version_model = 'td_maternal_validators.tdconsentversion'
        AntenatalVisitMembershipFormValidator.consent_version_model =\
            self.td_consent_version_model

    def test_consentversion_object_does_not_exist(self):
        '''Asserts if Validation Error is raised if the consent version object
        does not exist.'''

        self.td_consent_version.delete()
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier}
        form_validator = AntenatalVisitMembershipFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_consent_version_object_exists(self):
        '''Tests if consent version object exists, cleaned date validates
        or fails the tests if the Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier}
        form_validator = AntenatalVisitMembershipFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_maternal_consent_object_does_not_exist(self):
        '''Asserts if Validation Error is raised if the maternal consent object
        does not exist.'''

        self.subject_consent.delete()
        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier}
        form_validator = AntenatalVisitMembershipFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_maternal_consent_object_exists(self):
        '''Tests if maternal consent object exists, cleaned date validates
        or fails the tests if the Validation Error is raised unexpectedly.'''

        cleaned_data = {
            'subject_identifier': self.subject_consent.subject_identifier}
        form_validator = AntenatalVisitMembershipFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
