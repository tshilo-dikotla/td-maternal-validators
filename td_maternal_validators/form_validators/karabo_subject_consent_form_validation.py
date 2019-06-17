from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator


class KaraboSubjectConsentFormValidator(TDCRFFormValidator,
                                        FormValidator):

    maternal_subject_consent = 'td_maternal.subjectconsent'

    karabo_screening_model = 'td_maternal.karabosubjectscreening'

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_subject_consent)

    @property
    def karabo_screening_cls(self):
        return django_apps.get_model(self.karabo_screening_model)

    def clean(self):
        cleaned_data = self.cleaned_data
        self.maternal_identifier = cleaned_data.get('subject_identifier')
        self.subject_identifier = self.maternal_identifier + '-10'

        self.validate_against_screening_date(
            subject_identifier=self.maternal_identifier,
            report_datetime=cleaned_data.get('report_datetime'))

        self.required_if(
            NO,
            field='is_literate',
            field_required='guardian_name'
        )
        self.validate_maternal_name()
        self.validate_maternal_surname()
        self.validate_maternal_initials()
        self.validate_maternal_dob()
        self.validate_maternal_omang()
        self.clean_review_questions('consent_reviewed', NO)
        self.clean_review_questions('study_questions', NO)
        self.clean_review_questions('assessment_score', NO)
        self.clean_review_questions('consent_copy', NO)
        self.clean_review_questions('consent_signature', NO)

    def validate_against_screening_date(self, subject_identifier=None,
                                        report_datetime=None):

        try:
            karabo_screening = self.karabo_screening_cls.objects.get(
                subject_identifier=subject_identifier)
        except self.karabo_screening_cls.DoesNotExist:
            raise ValidationError(
                'Please complete Karabo Screening form '
                f'before  proceeding.')
        else:
            if report_datetime and report_datetime < karabo_screening.report_datetime:
                raise forms.ValidationError(
                    "Report datetime cannot be before Karabo Screening datetime.")
            else:
                return karabo_screening

    def validate_maternal_name(self):
        '''Validates maternal name from Tshilo dikotla and Karabo Study
        '''
        subject_identifier = self.cleaned_data.get('subject_identifier')

        try:
            maternal_consent = self.maternal_consent_cls.objects.get(
                subject_identifier=subject_identifier)
        except self.maternal_consent_cls.DoesNotExist:
            raise ValidationError({
                'subject_identifier': 'Subject Identifier doesn\'t'
                ' exists in Tshilo Dikotla'})
        else:
            if not self.cleaned_data['first_name'] == maternal_consent.first_name:
                raise ValidationError(
                    {'first_name': 'Please Enter Maternal First Name'
                     ' similar to Tshilo Dikotla'})

    def validate_maternal_surname(self):
        '''Validates maternal name from Tshilo dikotla and Karabo Study
        '''
        subject_identifier = self.cleaned_data.get('subject_identifier')
        try:
            maternal_consent = self.maternal_consent_cls.objects.get(
                subject_identifier=subject_identifier)

        except self.maternal_consent_cls.DoesNotExist:
            raise ValidationError(
                {'subject_identifier': 'Subject Identifier doesn\'t'
                 ' exists in Tshilo Dikotla'})

        else:
            if not self.cleaned_data['last_name'] == maternal_consent.last_name:
                raise ValidationError(
                    {'last_name': 'Please Enter Maternal Surname'
                     ' similar to Tshilo Dikotla'})

    def validate_maternal_initials(self):
        '''Validates maternal name from Tshilo dikotla and Karabo Study
        '''
        subject_identifier = self.cleaned_data.get('subject_identifier')

        try:
            maternal_consent = self.maternal_consent_cls.objects.get(
                subject_identifier=subject_identifier)

        except self.maternal_consent_cls.DoesNotExist:
            raise ValidationError(
                {'subject_identifier': 'Subject Identifier doesn\'t'
                 ' exists in Tshilo Dikotla'})
        else:
            if not self.cleaned_data['initials'] == maternal_consent.initials:
                raise ValidationError(
                    {'initials': 'Please Enter Maternal Initials'
                     ' similar to Tshilo Dikotla'})

    def validate_maternal_dob(self):
        '''Validates maternal name from Tshilo dikotla and Karabo Study
        '''
        subject_identifier = self.cleaned_data.get('subject_identifier')
        try:
            maternal_consent = self.maternal_consent_cls.objects.get(
                subject_identifier=subject_identifier)

        except self.maternal_consent_cls.DoesNotExist:
            raise ValidationError(
                {'subject_identifier': 'Subject Identifier doesn\'t'
                 ' exists in Tshilo Dikotla'})

        else:
            if not self.cleaned_data['dob'] == maternal_consent.dob:
                raise ValidationError(
                    {'dob': 'Please Enter Maternal Date of Birth'
                     ' similar to Tshilo Dikotla'})

    def validate_maternal_omang(self):
        '''Validates maternal name from Tshilo dikotla and Karabo Study
        '''
        subject_identifier = self.cleaned_data.get('subject_identifier')

        try:
            maternal_consent = self.maternal_consent_cls.objects.get(
                subject_identifier=subject_identifier)
        except self.maternal_consent_cls.DoesNotExist:
            raise ValidationError(
                {'subject_identifier': 'Subject Identifier doesn\'t'
                 ' exists in Tshilo Dikotla'})
        else:
            if not self.cleaned_data['identity'] == maternal_consent.identity:
                raise ValidationError(
                    {'identity': 'Please Enter Maternal identity'
                     ' similar to Tshilo Dikotla'})

    def clean_review_questions(self, field, response):
        cleaned_field = self.cleaned_data.get(field)
        if cleaned_field == response:
            raise forms.ValidationError({
                field:
                'Complete this part of the informed consent process '
                'before continuing.'})
