from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, NOT_APPLICABLE, MALE, YES, NO, NEG

from td_maternal.models.list_models import ChronicConditions, MaternalMedications, WcsDxAdult

from ..form_validators import MaternalMedicalHistoryFormValidator
from .models import (
    SubjectConsent, Appointment, MaternalVisit,
    RegisteredSubject, ListModel)


class MaternalStatusHelper:

    def __init__(self, status=None):
        self.status = status

    @property
    def hiv_status(self):
        return self.status


@tag('hist')
class TestMaternalMedicalHistoryForm(TestCase):

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
            appointment=appointment)

        self.registered_subject = RegisteredSubject.objects.create(
            first_name='First_Name', last_name='Last_Name', gender=MALE)

        self.subject_identifier = '12345ABC'

        ChronicConditions.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        ChronicConditions.objects.create(name=YES, short_name='y')
        MaternalMedications.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')
        WcsDxAdult.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        self.cleaned_data = {
            'cd4_count': None,
            'cd4_date': None,
            'is_date_estimated': None,
            'mother_chronic': ChronicConditions.objects.filter(name=NOT_APPLICABLE),
            'father_chronic': ChronicConditions.objects.filter(name=NOT_APPLICABLE),
            'mother_medications': MaternalMedications.objects.all(),
            'sero_posetive': None,
            'date_hiv_diagnosis': None,
            'perinataly_infected': NOT_APPLICABLE,
            'know_hiv_status': NOT_APPLICABLE,
            'who': WcsDxAdult.objects.all(),
            'lowest_cd4_known': NOT_APPLICABLE}

    def test_subject_status_neg(self):
        '''True if chronic_since is yes and who_diagnosis is no.
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=YES,
            who_diagnosis=NO
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_neg_valid(self):
        '''True if chronic_since is no and who_diagnosis is Not_applicable.
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_neg_invalid(self):
        '''Assert raises exception if chronic_since is none but who_diagnosis is yes.
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=YES,
            who_diagnosis=None,
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_neg_na_valid(self):
        '''True if chronic_since is none and who_diagnosis is Not_applicable.
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=None,
            who_diagnosis=NOT_APPLICABLE,
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_pos_valid(self):
        '''True if chronic_since is none and who_diagnosis is Not_applicable.
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=NOT_APPLICABLE,
            who_diagnosis=NOT_APPLICABLE,
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_pos_no_valid(self):
        '''True if chronic_since is none and who_diagnosis is Not_applicable.
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=NO,
            who_diagnosis=YES,
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_pos_yes_who_none(self):
        '''Assert raises exception if who is none and'
        'who_diagnosis is not_applicable.
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=YES,
            who_diagnosis=NOT_APPLICABLE,
            who=None
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_pos_yes_who_na(self):
        '''Assert raises exception if who has no list and'
        'who_diagnosis is not_applicable.
        '''
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE,
            who=WcsDxAdult.objects.all()
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_pos_yes_who_valid(self):
        '''Assert raises exception if who has a list and'
        'who_diagnosis is not_applicable.
        '''
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=YES,
            who_diagnosis=NOT_APPLICABLE,
            who=WcsDxAdult.objects.all()
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_pos_yes_who_list_yes(self):
        '''True if who has a list and who_diagnosis is yes.
        '''
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=YES,
            who_diagnosis=YES,
            who=WcsDxAdult.objects.all()
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_if_who_diagnosis_who_chronic_is_valid(self):
        '''True if subject_status is NEG and who_dianosis is NOT_APPLICABLE
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            who_diagnosis=NOT_APPLICABLE,
            who=ListModel.objects.all()
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who', form_validator._errors)

    def test_if_who_diagnosis_who_chronic_is_invalid(self):
        '''Assert raises exception if subject_status is NEG and who_dianosis is none
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            who_diagnosis=None,
            who=ListModel.objects.all()
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who', form_validator._errors)

    def test_if_who_diagnosis_who_chronic_is_invalid_none(self):
        '''True if subject_status is NEG and who_dianosis is none
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            who_diagnosis=None,
            who=NOT_APPLICABLE
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_if_who_diagnosis_who_chronic_is_invalid_pos(self):
        '''Assert raises exception if subject_status is NEG and who_dianosis
        is NOT_APPLICABLE
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            who_diagnosis=NOT_APPLICABLE,
            who=ListModel.objects.all()
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who', form_validator._errors)

    def test_if_mother_medication_true(self):
        '''True if mother_medication is true
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            mother_medication=True,
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_seropositive_invalid(self):
        '''Assert raises exception if sero_posetive is yes
        and date_hiv_diagnosis is not given
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=YES,
            date_hiv_diagnosis=None
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sero_posetive', form_validator._errors)

    def test_validate_positive_mother_seropositive_yes(self):
        '''Assert raises exception if sero_posetive is yes and perinataly_infected,
        know_hiv_status, lowest_cd4_known are given
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=YES,
            perinataly_infected=YES,
            know_hiv_status=YES,
            lowest_cd4_known=YES
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sero_posetive', form_validator._errors)

    def test_validate_positive_mother_seropositive_no(self):
        '''True if sero_posetive is no and perinataly_infected, know_hiv_status,
        lowest_cd4_known are not applicable
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=NO,
            perinataly_infected=NOT_APPLICABLE,
            know_hiv_status=NOT_APPLICABLE,
            lowest_cd4_known=NOT_APPLICABLE
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_negative_mother_seropositive_no_cd4_not(self):
        '''True if sero_posetive is no and perinataly_infected,
        know_hiv_status are not given, but lowest_cd4_known is given
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=NO,
            cd4_date=None,
            cd4_count=None,
            is_date_estimated=None,
            lowest_cd4_known=NOT_APPLICABLE
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_negative_no_cd4_not(self):
        '''Assert raises exception if sero_posetive is yes and perinataly_infected,
        know_hiv_status, lowest_cd4_known are given
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=YES,
            cd4_date=get_utcnow().date() + relativedelta(years=1),
            cd4_count=20,
            is_date_estimated=get_utcnow().date() + relativedelta(years=2),
            lowest_cd4_known=NOT_APPLICABLE
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sero_posetive', form_validator._errors)

    def test_validate_negative_no_cd4_invalid(self):
        '''True if sero_posetive is no and perinataly_infected, know_hiv_status,
        lowest_cd4_known are not given
        '''
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=NO,
            cd4_date=None,
            cd4_count=None,
            is_date_estimated=None,
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_negative_mother_seropositive_no(self):
        '''Assert raises exception if sero_posetive is yes
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=YES,
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sero_posetive', form_validator._errors)

    def test_validate_seropositive_date_hiv_diagnosis(self):
        '''Assert raises exception if sero_posetive is yes and date_hiv_diagnosis is
        given
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=YES,
            date_hiv_diagnosis=get_utcnow()
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sero_posetive', form_validator._errors)

    def test_validate_seropositive_date_hiv_diagnosis_valid(self):
        '''True if sero_posetive is yes and date_hiv_diagnosis is not given
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=NO,
            date_hiv_diagnosis=None
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_seropositive_perinataly_infected_valid(self):
        '''True if sero_posetive is yes and date_hiv_diagnosis is not given
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=NO,
            perinataly_infected=NOT_APPLICABLE
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_seropositive_perinataly_infected_invalid(self):
        '''Assert raises exception if sero_posetive is yes and perinataly_infected
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=YES,
            perinataly_infected=YES
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sero_posetive', form_validator._errors)

    def test_validate_seropositive_know_hiv_status_invalid(self):
        '''Assert raises exception if sero_posetive is yes and know_hiv_status is yes
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=YES,
            know_hiv_status=YES
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sero_posetive', form_validator._errors)

    def test_validate_seropositive_know_hiv_status_valid(self):
        '''True if sero_posetive is yes and know_hiv_status is NOT applicable
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=NO,
            know_hiv_status=NOT_APPLICABLE
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_validate_lowest_cd4_known_valid(self):
        '''True if the lowest_cd4 is NOT applicable when the status is POS
        '''
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=YES,
            lowest_cd4_known=NOT_APPLICABLE
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('lowest_cd4_known', form_validator._errors)

    def test_validate_lowest_cd4_known_invalid(self):
        '''Assert raises exception if the status is NEG and lowest_cd4 is not Applicable
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            lowest_cd4_known=NOT_APPLICABLE
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'VallidationError unexpectedly raised. Got{e}')
