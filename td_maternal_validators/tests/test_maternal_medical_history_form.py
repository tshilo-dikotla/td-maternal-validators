from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, NOT_APPLICABLE, MALE, YES, NO, NEG

from td_maternal.models.list_models import ChronicConditions, MaternalMedications, WcsDxAdult

from ..form_validators import MaternalMedicalHistoryFormValidator
from .models import (
    SubjectConsent, Appointment, MaternalVisit,
    RegisteredSubject, ListModel, AntenatalEnrollment)


class MaternalStatusHelper:

    def __init__(self, status=None):
        self.status = status

    @property
    def hiv_status(self):
        return self.status


@tag('hist')
class TestMaternalMedicalHistoryForm(TestCase):

    def setUp(self):
        MaternalMedicalHistoryFormValidator.antenatal_enrollment_model = \
            'td_maternal_validators.antenatalenrollment'

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

        AntenatalEnrollment.objects.create(
            week32_test_date=get_utcnow().date(),
            subject_identifier=self.subject_consent.subject_identifier)
        WcsDxAdult.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        self.cleaned_data = {
            'maternal_visit': self.maternal_visit,
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

    def test_subject_status_neg_chronic_since_invalid(self):
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
        self.assertIn('chronic_since', form_validator._errors)

    def test_subject_status_neg_who_diagnosis_invalid(self):
        '''True if chronic_since is yes and who_diagnosis is no.
        '''
        maternal_status = MaternalStatusHelper(status=NEG)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=NO,
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
        '''Assert raises exception if chronic_since is provided but
         who_diagnosis is not applicable.
        '''
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper =\
            maternal_status
        self.cleaned_data.update(
            chronic_since=YES,
            who_diagnosis=NOT_APPLICABLE,
            lowest_cd4_known=10
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who_diagnosis', form_validator._errors)

    def test_subject_status_pos_na_who_none(self):
        '''Assert raises exception if who is provided but
        who_diagnosis is NO.
        '''
        ListModel.objects.create(name='blahblah')
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            chronic_since=NO,
            who_diagnosis=NO,
            sero_posetive=YES,
            lowest_cd4_known=YES,
            perinataly_infected=NO,
            date_hiv_diagnosis=get_utcnow(),
            know_hiv_status=YES,
            cd4_count=50,
            who=ListModel.objects.all()
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who', form_validator._errors)

    def test_subject_status_pos_na_who_none_invalid(self):
        '''Assert raises exception if who is provided but
        who_diagnosis is NO.
        '''
        ListModel.objects.create(name=NOT_APPLICABLE)
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            maternal_visit=self.maternal_visit,
            chronic_since=YES,
            who_diagnosis=YES,
            sero_posetive=YES,
            lowest_cd4_known=YES,
            perinataly_infected=NO,
            date_hiv_diagnosis=get_utcnow().date(),
            know_hiv_status=YES,
            is_date_estimated=NO,
            cd4_count=50,
            cd4_date=get_utcnow(),
            who=ListModel.objects.filter(name=NOT_APPLICABLE)
        )
        form_validator = MaternalMedicalHistoryFormValidator(
            cleaned_data=self.cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who', form_validator._errors)

    def test_subject_status_pos_who_valid(self):
        '''Assert raises exception if who is provided but
        who_diagnosis is NO.
        '''
        ListModel.objects.create(name='blahblah')
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            maternal_visit=self.maternal_visit,
            chronic_since=YES,
            who_diagnosis=YES,
            sero_posetive=YES,
            lowest_cd4_known=YES,
            perinataly_infected=NO,
            date_hiv_diagnosis=get_utcnow().date(),
            know_hiv_status=YES,
            cd4_count=50,
            is_date_estimated=NO,
            cd4_date=get_utcnow(),
            who=ListModel.objects.all()
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

    def test_negative_mother_seropositive_no(self):
        '''Assert raises exception if sero_posetive is yes
        '''
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            sero_posetive=NO,
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

    def test_validate_lowest_cd4_known_valid(self):
        '''True if the lowest_cd4 is NOT applicable when the status is POS
        '''
        maternal_status = MaternalStatusHelper(status=POS)
        MaternalMedicalHistoryFormValidator.maternal_status_helper = maternal_status
        self.cleaned_data.update(
            date_hiv_diagnosis=get_utcnow(),
            sero_posetive=YES,
            lowest_cd4_known=NOT_APPLICABLE,
            perinataly_infected=YES,
            know_hiv_status=YES
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
