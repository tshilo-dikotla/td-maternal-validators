from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, OTHER

from ..form_validators import MaternalSrhFormValidator
from .models import SubjectConsent, MaternalVisit, ListModel, Appointment


class TestMaternalSrhForm(TestCase):

    def setUp(self):
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow())

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,)

    def test_is_contraceptive_initiated(self):
        ListModel.objects.create(name='pills', short_name='Pills')
        ListModel.objects.create(name='iud', short_name='IUD')

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'seen_at_clinic': YES,
            'is_contraceptive_initiated': None
        }
        form_validator = MaternalSrhFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('is_contraceptive_initiated', form_validator._errors)

    def test_other_reason_unseen_clinic_required(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'seen_at_clinic': NO,
            'reason_unseen_clinic': OTHER,
            'reason_unseen_clinic_other': None
        }
        form_validator = MaternalSrhFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_reason_not_initiated_other_required(self):
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'seen_at_clinic': YES,
            'reason_not_initiated': OTHER,
            'reason_not_initiated_other': None
        }
        form_validator = MaternalSrhFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_is_contr_init_YES_contr_list_required(self):
        ListModel.objects.create(name='pills', short_name='Pills')
        ListModel.objects.create(name='iud', short_name='IUD')

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_contraceptive_initiated': YES,
            'contr': None
        }
        form_validator = MaternalSrhFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contr', form_validator._errors)

    def test_is_contr_init_YES_contr_list_provided(self):
        ListModel.objects.create(name='pills', short_name='Pills')
        ListModel.objects.create(name='iud', short_name='IUD')

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'is_contraceptive_initiated': YES,
            'contr': ListModel.objects.all()
        }
        form_validator = MaternalSrhFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
