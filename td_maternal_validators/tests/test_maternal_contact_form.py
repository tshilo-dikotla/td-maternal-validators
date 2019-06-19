from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import MaternalContactFormValidator
from .models import MaternalLocator, SubjectConsent, SubjectScreening
from .models import MaternalVisit, Appointment, TdConsentVersion


@tag('mcon')
class TestMaternalContactForm(TestCase):

    def setUp(self):
        MaternalContactFormValidator.maternal_consent_model = \
            'td_maternal_validators.subjectconsent'
        MaternalContactFormValidator.consent_version_model = \
            'td_maternal_validators.tdconsentversion'
        MaternalContactFormValidator.subject_screening_model = \
            'td_maternal_validators.subjectscreening'
        MaternalContactFormValidator.maternal_locator_model = \
            'td_maternal_validators.maternallocator'

        self.subject_identifier = '11111111'

        self.subject_screening = SubjectScreening.objects.create(
            subject_identifier='11111111',
            screening_identifier='ABC12345',
            age_in_years=22)

        self.consent_version = TdConsentVersion.objects.create(
            screening_identifier='ABC12345',
            version='3')

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111', screening_identifier='ABC12345',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(), version='3')

        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_consent.subject_identifier)

        self.maternal_locator = MaternalLocator.objects.create(
            subject_identifier='11111111',
            may_call=YES,
            may_sms=YES)

    def test_contact_form_valid(self):
        '''Assert form saves without error.
        '''
        cleaned_data = {
            'subject_identifier': '11111111',
        }
        form_validator = MaternalContactFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_contact_form_call_invalid(self):
        '''Assert form saves without error.
        '''
        self.maternal_locator.may_call = NO
        self.maternal_locator.save()
        cleaned_data = {
            'subject_identifier': '11111111',
            'contact_type': 'voice_call'
        }
        form_validator = MaternalContactFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contact_type', form_validator._errors)

    def test_contact_form_text_invalid(self):
        '''Assert form saves without error.
        '''
        self.maternal_locator.may_sms = NO
        self.maternal_locator.save()
        cleaned_data = {
            'subject_identifier': '11111111',
            'contact_type': 'text_message'
        }
        form_validator = MaternalContactFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contact_type', form_validator._errors)

    def test_contact_success_invalid(self):
        '''Assert form saves without error.
        '''
        cleaned_data = {
            'subject_identifier': '11111111',
            'contact_type': 'text_message',
            'contact_success': YES,
            'contact_comment': None
        }
        form_validator = MaternalContactFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contact_comment', form_validator._errors)

    def test_contact_success_valid(self):
        '''Assert form saves without error.
        '''
        cleaned_data = {
            'subject_identifier': '11111111',
            'contact_type': 'text_message',
            'contact_success': NO,
            'contact_comment': None

        }
        form_validator = MaternalContactFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_contact_success_valid2(self):
        '''Assert form saves without error.
        '''
        cleaned_data = {
            'subject_identifier': '11111111',
            'contact_type': 'text_message',
            'contact_success': NO,
            'contact_comment': None

        }
        form_validator = MaternalContactFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
