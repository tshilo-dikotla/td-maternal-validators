from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from .models import (
    MaternalConsent, Appointment, MaternalVisit, MaternalUltraSoundInitial)
from ..form_validators import MaternalObstericalHistoryFormValidator


class TestMaternalObstericalHistoryForm(TestCase):
    def setUp(self):
        self.subject_consent = MaternalConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment)
        MaternalUltraSoundInitial.objects.create(
            maternal_visit=self.maternal_visit, ga_confirmed=20)

    def test_ultrasound_blank_invalid(self):
        '''Asserts raises exception if ultrasound form has been left blank.'''

        cleaned_data = {
            'ultrasound': None, }
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ultrasound', form_validator._errors)

    def test_ultrasound_not_blank_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.all()}
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_prev_preg_one_pregs_24wks_or_more_not_zero(self):
        '''Asserts raises exception if previous pregnancies is 1
        and and the value of pregnancies 24 weeks or more is not 0.'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.filter(
                maternal_visit=self.maternal_visit),
            'prev_pregnancies': 1,
            'pregs_24wks_or_more': 3}
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pregs_24wks_or_more', form_validator._errors)

    def test_prev_preg_one_lost_before_24wks_not_zero(self):
        '''Asserts raises exception if previous pregnancies is 1
        and and the value of pregnancies lost before 24 weeks is not 0.'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.filter(
                maternal_visit=self.maternal_visit),
            'prev_pregnancies': 1,
            'lost_before_24wks': 2}
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('lost_before_24wks', form_validator._errors)

    def test_prev_preg_one_lost_after_24wks_not_zero(self):
        '''Asserts raises exception if previous pregnancies is 1
        and and the value of pregnancies lost after 24 weeks is not 0.'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.filter(
                maternal_visit=self.maternal_visit),
            'prev_pregnancies': 1,
            'lost_after_24wks': 2}
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('lost_after_24wks', form_validator._errors)

    def test_sum_pregs_lost_before_and_current_preg_sum_not_equal(self):
        '''Asserts raises exception if the sum of pregnancies 24 weeks or more
        and pregnancies lost before 24 weeks is not equals to the value of
        previous pregnancies.'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.filter(
                maternal_visit=self.maternal_visit),
            'prev_pregnancies': 2,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 2,
            'lost_after_24wks': 1}
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_sum_pregs_lost_before_and_current_preg_sum_equal(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.filter(
                maternal_visit=self.maternal_visit),
            'prev_pregnancies': 3,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 2,
            'lost_after_24wks': 1}
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pregs_24wks_less_than_lost_after(self):
        '''Asserts raises exception if pregnancies 24 weeks or more
        is less than pregnancies lost before 24 weeks.'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.filter(
                maternal_visit=self.maternal_visit),
            'prev_pregnancies': 3,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 2,
            'lost_after_24wks': 2}
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pregs_24wks_or_more', form_validator._errors)

    def test_sum_pregs_24wks_not_less_than_lost_after(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.filter(
                maternal_visit=self.maternal_visit),
            'prev_pregnancies': 23,
            'pregs_24wks_or_more': 21,
            'lost_before_24wks': 2,
            'lost_after_24wks': 2}
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_sum_deliv_37wks_invalid(self):
        '''Asserts raises exception if the sum of Q8 and Q9 is not equal to'
        '(Q2 -1) - (Q4 + Q5)'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.filter(
                maternal_visit=self.maternal_visit),
            'children_deliv_before_37wks': 7,
            'children_deliv_aftr_37wks': 5,
            'lost_before_24wks': 1,
            'lost_after_24wks': 2,
            'pregs_24wks_or_more': 4,
            'prev_pregnancies': 15}
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_sum_deliv_37wks_valid(self):
        '''Tests if cleaned data validates or fails tests if exception
        is raised unexpectedly.'''

        cleaned_data = {
            'ultrasound': MaternalUltraSoundInitial.objects.filter(
                maternal_visit=self.maternal_visit),
            'children_deliv_before_37wks': 3,
            'children_deliv_aftr_37wks': 2,
            'lost_before_24wks': 1,
            'lost_after_24wks': 2,
            'prev_pregnancies': 9,
            'pregs_24wks_or_more': 8, }
        form_validator = MaternalObstericalHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
