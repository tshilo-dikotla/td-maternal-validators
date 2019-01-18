from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import (YES, NO, NOT_APPLICABLE, NEG, POS, FEMALE)
from .models import (MaternalConsent, MaternalVisit, ListModel, Appointment,
                     RapidTestResult, AntenatalEnrollment, RegisteredSubject)
from ..form_validators import MaternalPostPartumFuFormValidator


@tag('p')
class TestMaternalPostPartumFuForm(TestCase):
    def setUp(self):
        self.subject_consent = MaternalConsent.objects.create(
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
            first_name='Ame', last_name='Diphoko', gender=FEMALE)
        self.rapid_test_result = RapidTestResult.objects.create(
            maternal_visit=self.maternal_visit, result=NEG)
        self.rapid_test_result_model = 'td_maternal_validators.rapidtestresult'
        MaternalPostPartumFuFormValidator.rapid_test_result_model = \
            self.rapid_test_result_model
        self.subject_identifier = '12345ABC'
        self.enrollment_status = AntenatalEnrollment.objects.create(
            subject_identifier=self.subject_identifier, enrollment_hiv_status=POS)
        self.antenatal_enrollment_model = 'td_maternal_validators.antenatalenrollment'
        MaternalPostPartumFuFormValidator.antenatal_enrollment_model = \
            self.antenatal_enrollment_model

    def test_hospitalized_yes_reason_required(self):
        '''Asserts if an exception is raised if subject has been hospitalized
        but the hospitalization reason is missing.'''

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': None,
            'hospitalization_days': 10,
            'diagnoses': ListModel.objects.create(
                name=NOT_APPLICABLE, short_name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_yes_reason_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''
        ListModel.objects.create(
            name='hypertension', short_name='hypertension')
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(
                name='hypertension'),
            'hospitalization_days': 10,
            'diagnoses': ListModel.objects.filter(
                name=NOT_APPLICABLE),
            'has_who_dx': NOT_APPLICABLE,
            'who': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hospitalized_yes_reason_na_invalid(self):
        '''Asserts if an exception is raised if subject has been hospitalized
        but the hospitalization reason list selection is N/A.'''

        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': 10,
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_no_reason_na_valid(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': None,
            'diagnoses': ListModel.objects.all(),
            'has_who_dx': NOT_APPLICABLE,
            'who': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hospitalized_no_reason_list_invalid(self):
        '''Asserts if an exception is raised if subject has not been hospitalized
        but the hospitalization reason is provided.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': None,
            'diagnoses': ListModel.objects.filter(
                name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_reason', form_validator._errors)

    def test_hospitalized_yes_number_of_days_required(self):
        '''Asserts if an exception is raised if subject has been hospitalized
        but the hospitalization days are missing.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(
                name='hypertension'),
            'hospitalization_days': None,
            'diagnoses': ListModel.objects.filter(
                name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_days', form_validator._errors)

    def test_hospitalized_yes_number_of_days_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(
            name='hypertension', short_name='hypertension')
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(
                name='hypertension'),
            'hospitalization_days': get_utcnow().date(),
            'diagnoses': ListModel.objects.filter(
                name=NOT_APPLICABLE),
            'has_who_dx': NOT_APPLICABLE,
            'who': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hospitalized_no_number_of_days_invalid(self):
        '''Asserts if an exception is raised if subject has not been hospitalized
        but the hospitalization days are provided.'''
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': get_utcnow().date(),
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hospitalization_days', form_validator._errors)

    def test_hospitalized_no_number_of_days_none_valid(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''
        ListModel.objects.create(
            name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'hospitalized': NO,
            'hospitalization_reason': ListModel.objects.all(),
            'hospitalization_days': None,
            'diagnoses': ListModel.objects.all(),
            'has_who_dx': NOT_APPLICABLE,
            'who': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diagnoses_required(self):
        '''Asserts if an exception is raised if required field diagnoses
        is missing.'''
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'hospitalization_reason': ListModel.objects.all(),
            'diagnoses': None}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diagnoses', form_validator._errors)

    def test_new_diagnoses_yes_diagnoses_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''
        ListModel.objects.create(name='cancer', short_name='cancer')
        ListModel.objects.create(name='sick', short_name='sick')
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(name='sick'),
            'hospitalization_days': get_utcnow().date(),
            'new_diagnoses': YES,
            'diagnoses': ListModel.objects.filter(name='cancer'),
            'has_who_dx': NOT_APPLICABLE,
            'who': ListModel.objects.filter(name=NOT_APPLICABLE)
        }
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_new_diagnoses_yes_diagnosis_na_invalid(self):
        '''Asserts if an exception is raised if new diagnoses is yes
        but the diagnoses list selection is N/A.'''
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        ListModel.objects.create(name='sick', short_name='sick')
        cleaned_data = {
            'hospitalized': YES,
            'hospitalization_reason': ListModel.objects.filter(name='sick'),
            'hospitalization_days': get_utcnow().date(),
            'new_diagnoses': YES,
            'diagnoses': ListModel.objects.filter(name=NOT_APPLICABLE),
            'has_who_dx': NOT_APPLICABLE,
            'who': ListModel.objects.filter(name=NOT_APPLICABLE)}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diagnoses', form_validator._errors)

    def test_new_diagnoses_no_diagnoses_na_valid(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'hospitalization_reason': ListModel.objects.all(),
            'new_diagnoses': NO,
            'diagnoses': ListModel.objects.all(),
            'has_who_dx': NOT_APPLICABLE,
            'who': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_diagnoses_no_diagnoses_list_invalid(self):
        '''Asserts if an exception is raised if new diagnoses is No
        but the diagnoses list selection includes N/A.'''
        ListModel.objects.create(name='cancer', short_name='cancer')
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'hospitalization_reason': ListModel.objects.filter(
                name=NOT_APPLICABLE, short_name='N/A'),
            'new_diagnoses': NO,
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diagnoses', form_validator._errors)

    def test_diagnoses_no_diagnoses_invalid(self):
        '''Asserts if an exception is raised if new diagnoses is No
        but the diagnoses list selection includes N/A.'''

        ListModel.objects.create(name='cancer', short_name='cancer')

        cleaned_data = {
            'hospitalization_reason': ListModel.objects.create(
                name=NOT_APPLICABLE, short_name='N/A'),
            'new_diagnoses': NO,
            'diagnoses': ListModel.objects.all()}
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('diagnoses', form_validator._errors)

    def test_subject_status_neg_has_who_dx_is_na(self):
        '''Asserts if an exception is raised if the subject's hiv status is
        negative but new diagnoses listed in the WHO Adult/Adolescent HIV
        clinical staging document is not N/A.'''
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hospitalization_reason': ListModel.objects.all(),
            'diagnoses': ListModel.objects.all(),
            'has_who_dx': YES,
            'who': None
        }
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('has_who_dx', form_validator._errors)

    def test_subject_status_neg_has_who_dx_na(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hospitalization_reason': ListModel.objects.all(),
            'diagnoses': ListModel.objects.all(),
            'has_who_dx': NOT_APPLICABLE,
            'who': ListModel.objects.all()
        }

        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_pos_has_who_dx_applicable(self):
        '''Asserts if an exception is raised if the subject's hiv status is
        positive but new diagnoses listed in the WHO Adult/Adolescent HIV
        clinical staging document is N/A.'''
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hospitalization_reason': ListModel.objects.all(),
            'diagnoses': ListModel.objects.all(),
            'has_who_dx': NOT_APPLICABLE
        }
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('has_who_dx', form_validator._errors)

    def test_subject_status_pos_has_who_dx_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hospitalization_reason': ListModel.objects.all(),
            'diagnoses': ListModel.objects.all(),
            'has_who_dx': NO,
            'who': ListModel.objects.all()
        }
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_pos_has_who_dx_yes_who_required(self):
        '''Asserts if an exception is raised if the subject's hiv status is
        positive and new diagnoses listed in the WHO Adult/Adolescent HIV
        clinical staging document is YES but list of new WHO Stage III/IV
        diagnoses is not provided.'''
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hospitalization_reason': ListModel.objects.all(),
            'diagnoses': ListModel.objects.all(),
            'has_who_dx': YES,
            'who': ListModel.objects.all()
        }
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who', form_validator._errors)

    def test_subject_status_pos_has_who_dx_yes_who_provided(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''

        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        ListModel.objects.create(name='who', short_name='who')
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hospitalization_reason': ListModel.objects.filter(name=NOT_APPLICABLE),
            'diagnoses': ListModel.objects.filter(name=NOT_APPLICABLE),
            'has_who_dx': YES,
            'who': ListModel.objects.filter(name='who')
        }
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_subject_status_pos_has_who_dx_no_who_invalid(self):
        '''Asserts if an exception is raised if the subject's hiv status is
        positive and new diagnoses listed in the WHO Adult/Adolescent HIV
        clinical staging document is NO but list of new WHO Stage III/IV
        diagnoses is provided.'''

        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        ListModel.objects.create(name='who', short_name='who')
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hospitalization_reason': ListModel.objects.filter(name=NOT_APPLICABLE),
            'diagnoses': ListModel.objects.filter(name=NOT_APPLICABLE),
            'has_who_dx': NO,
            'who': ListModel.objects.all()
        }
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('who', form_validator._errors)

    def test_subject_status_pos_has_who_dx_no_who_valid(self):
        '''Tests if the cleaned data validates or fails the tests if Validation
        Error is raised unexpectedly.'''
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        self.rapid_test_result.result = POS
        self.rapid_test_result.save()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hospitalization_reason': ListModel.objects.all(),
            'diagnoses': ListModel.objects.all(),
            'has_who_dx': NO,
            'who': ListModel.objects.all()
        }
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_rapid_testing_result_does_not_exist(self):
        '''Asserts raises exception if rapid testing result model object
        does not exist.'''
        ListModel.objects.create(name=NOT_APPLICABLE, short_name='N/A')

        self.rapid_test_result.delete()
        cleaned_data = {
            'maternal_visit': self.maternal_visit,
            'hospitalization_reason': ListModel.objects.all(),
            'diagnoses': ListModel.objects.all(),
        }
        form_validator = MaternalPostPartumFuFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
