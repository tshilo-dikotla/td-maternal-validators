from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, NO

from ..form_validators import SpecimenConsentFormValidator
from .models import SubjectConsent, TdConsentVersion


class TestSpecimenConsent(TestCase):

    def setUp(self):
        SpecimenConsentFormValidator.consent_model_cls = SubjectConsent
        SpecimenConsentFormValidator.consent_version_model = TdConsentVersion

        self.consent_version = TdConsentVersion.objects.create(
            screening_identifier='ABC12345',
            version='3')

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            is_literate=YES, consent_datetime=get_utcnow(), version='3')

    def test_consent_required(self):
        self.subject_consent = None

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow()}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_illiterate_witness_required_invalid(self):

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            is_literate=NO, consent_datetime=get_utcnow(), version='3')

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow(),
            'is_literate': NO,
            'witness_name': None}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('witness_name', form_validator._errors)

    def test_illiterate_witness_required_valid(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            is_literate=NO, witness_name='blah blah',
            consent_datetime=get_utcnow(), version='3')

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow(),
            'is_literate': NO,
            'witness_name': 'blah blah'}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_study_consent_literate_invalid(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            is_literate=YES, witness_name='blah blah',
            consent_datetime=get_utcnow(), version='3')

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow(),
            'is_literate': NO,
            'witness_name': 'blah blah'}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is literate', form_validator._errors)

    def test_study_consent_witness_name_invalid(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            is_literate=NO, consent_datetime=get_utcnow(), version='3')

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow(),
            'is_literate': NO,
            'witness_name': 'blah blah'}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('witness name', form_validator._errors)

    def test_purpose_explained_invalid(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            is_literate=YES, witness_name=None,
            consent_datetime=get_utcnow(), version='3')

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow(),
            'is_literate': YES,
            'may_store_samples': YES}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('purpose_explained', form_validator._errors)

    def test_purpose_explained_understood_valid(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            is_literate=YES, witness_name=None,
            consent_datetime=get_utcnow(), version='3')

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow(),
            'is_literate': YES,
            'may_store_samples': YES,
            'purpose_explained': YES,
            'purpose_understood': YES}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_purpose_understood_invalid(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            witness_name=None, is_literate=YES, consent_datetime=get_utcnow(),
            version='3')

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow(),
            'is_literate': YES,
            'may_store_samples': YES,
            'purpose_explained': YES}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('purpose_understood', form_validator._errors)

    def test_copy_of_consent_provided_valid(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            is_literate=YES, witness_name=None,
            consent_datetime=get_utcnow(), version='3')

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow(),
            'is_literate': YES,
            'may_store_samples': YES,
            'purpose_explained': YES,
            'purpose_understood': YES,
            'offered_copy': YES}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_copy_of_consent_provided_invalid(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            witness_name=None, is_literate=YES, consent_datetime=get_utcnow(),
            version='3')

        cleaned_data = {
            'subject_identifier': '11111111',
            'consent_datetime': get_utcnow(),
            'is_literate': YES,
            'may_store_samples': NO,
            'purpose_explained': YES,
            'offered_copy': YES}
        form_validator = SpecimenConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('offered_copy', form_validator._errors)
