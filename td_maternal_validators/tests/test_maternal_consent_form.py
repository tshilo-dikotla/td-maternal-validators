from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import YES, NO, OTHER
from ..form_validators import MaternalConsentFormValidator
from .models import SubjectScreening, TdConsentVersion
from edc_base.utils import get_utcnow, relativedelta


@tag('consent')
class TestMaternalConsentForm(TestCase):

    def setUp(self):
        self.screening_identifier = 'ABC12345'
        self.subjectscreening = SubjectScreening.objects.create(
            screening_identifier=self.screening_identifier, has_omang=YES,
            age_in_years=22)
        self.subject_screening_model = 'td_maternal_validators.subjectscreening'
        MaternalConsentFormValidator.screening_model = self.subject_screening_model
        self.td_consent_version = TdConsentVersion.objects.create(
            subjectscreening=self.subjectscreening, version='1')
        self.consent_model = 'td_maternal_validators.tdconsentversion'
        MaternalConsentFormValidator.consent_model = self.consent_model

    def test_citizen_matches_has_omang(self):
        # N.B : has_omang in subject screening is set to YES
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'citizen': YES}
        form_validator = MaternalConsentFormValidator(
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
            'citizen': NO}
        form_validator = MaternalConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('citizen', form_validator._errors)

    def test_screening_age_mismatch_consent_dob_years(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=20)).date(),
            'citizen': YES}
        form_validator = MaternalConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)

    def test_screening_age_match_consent_dob_years(self):
        cleaned_data = {
            'screening_identifier': self.screening_identifier,
            'consent_datetime': get_utcnow(),
            'dob': (get_utcnow() - relativedelta(years=22)).date(),
            'citizen': YES}
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
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
            'citizen': YES
        }
        form_validator = MaternalConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)