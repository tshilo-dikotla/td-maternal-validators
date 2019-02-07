from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta

from ..form_validators import AntenatalVisitMembershipFormValidator
from .models import TdConsentVersion, SubjectScreening, SubjectConsent


class TestAntenatalVisitMembershipForm(TestCase):

    def setUp(self):
        AntenatalVisitMembershipFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        AntenatalVisitMembershipFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        AntenatalVisitMembershipFormValidator.subject_screening_model = \
            'td_maternal_validators.subjectscreening'

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')

        self.subject_screening = SubjectScreening.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            screening_identifier='ABC12345',
            age_in_years=22)

        self.td_consent_version = TdConsentVersion.objects.create(
            screening_identifier=self.subject_screening.screening_identifier,
            version='3', report_datetime=get_utcnow())

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
