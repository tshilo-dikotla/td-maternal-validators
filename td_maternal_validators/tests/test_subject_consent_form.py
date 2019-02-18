from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES, NO, OTHER

from ..form_validators import SubjectConsentFormValidator
from .models import SubjectScreening, TdConsentVersion


class TestSubjectConsentForm(TestCase):

    def setUp(self):
        self.screening_identifier = 'ABC12345'
        self.subjectscreening = SubjectScreening.objects.create(
            screening_identifier=self.screening_identifier, has_omang=YES,
            age_in_years=22)
        subject_screening_model = 'td_maternal_validators.subjectscreening'
        SubjectConsentFormValidator.screening_model = subject_screening_model
        self.td_consent_version = TdConsentVersion.objects.create(
            screening_identifier=self.screening_identifier, version='1')
        td_consent_version_model = 'td_maternal_validators.tdconsentversion'
        SubjectConsentFormValidator.td_consent_version_model =\
            td_consent_version_model

    def test_citizen_matches_has_omang(self):
        # N.B : has_omang in subject screening is set to YES
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES}
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_citizen_does_not_match_has_omang(self):
        # N.B : has_omang in subject screening is set to YES
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': NO}
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('citizen', form_validator._errors)

    def test_screening_age_mismatch_consent_dob_years(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=20)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES}
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)

    def test_screening_age_match_consent_dob_years(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES}
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_recruit_source_OTHER_source_other_required(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'recruit_source': OTHER,
            'recruit_source_other': None,
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruit_source_other', form_validator._errors)

    def test_recruit_source_OTHER_source_other_provided(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'recruit_source': OTHER,
            'recruit_source_other': 'family friend',
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_recruit_source_not_OTHER_source_other_invalid(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'recruit_source': 'ANC clinic staff',
            'recruit_source_other': 'family friend',
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruit_source_other', form_validator._errors)

    def test_recruit_source_not_OTHER_source_other_valid(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'recruit_source': 'ANC clinic staff',
            'recruit_source_other': None,
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_recruitment_clinic_OTHER_recruitment_clinic_other_required(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'recruitment_clinic': OTHER,
            'recruitment_clinic_other': None,
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruitment_clinic_other', form_validator._errors)

    def test_recruitment_clinic_OTHER_recruitment_clinic_other_provided(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'recruitment_clinic': OTHER,
            'recruitment_clinic_other': 'PMH',
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_recruitment_clinic_not_OTHER_recruitment_clinic_other_invalid(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'recruitment_clinic': 'PMH',
            'recruitment_clinic_other': 'G.West Clinic',
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recruitment_clinic_other', form_validator._errors)

    def test_recruitment_clinic_not_OTHER_recruitment_clinic_other_valid(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'recruitment_clinic': 'G.West Clinic',
            'recruitment_clinic_other': None,
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_current_consent_version_valid(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_current_consent_version_not_exist(self):
        self.td_consent_version.delete()

        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'citizen': YES
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_first_name_last_name_valid(self):

        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'citizen': YES,
            'first_name': 'TEST BONE',
            'last_name': 'TEST',
            'initials': 'TOT'
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('initials', form_validator._errors)

    def test_first_name_last_name_invalid(self):

        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'citizen': YES,
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT'
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_first_name_invalid(self):

        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'citizen': YES,
            'first_name': 'TEST ONE BEST',
            'last_name': 'TEST',
            'initials': 'TOT'
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('first_name', form_validator._errors)

    def test_first_name_valid(self):

        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'citizen': YES,
            'first_name': 'TEST ONE-BEST',
            'last_name': 'TEST',
            'initials': 'TOT'
        }
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
