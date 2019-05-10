from django.apps import apps as django_apps
from django import forms
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator


class KaraboSubjectConsentFormValidator(FormValidator):

    maternal_subject_consent = 'td_maternal.subjectconsent'

    def clean(self):

        self.required_if(
            NO,
            field='literacy',
            field_required='witness_name'
        )
        self.validate_maternal_name()
        self.validate_maternal_surname()
        self.validate_maternal_initials()
        self.validate_maternal_omang()
        self.clean_consent_reviewed()
        self.clean_study_questions()
        self.clean_consent_copy()
        self.clean_consent_signature()

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_subject_consent)

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

    def clean_consent_reviewed(self):
        consent_reviewed = self.cleaned_data.get('consent_reviewed')
        if consent_reviewed != YES:
            raise forms.ValidationError({
                'consent_reviewed':
                'Complete this part of the informed consent process '
                'before continuing.'})

    def clean_study_questions(self):
        study_questions = self.cleaned_data.get('study_questions')
        if study_questions != YES:
            raise forms.ValidationError({
                'study_questions':
                'Complete this part of the informed consent process'
                ' before continuing.'})

    def clean_consent_copy(self):
        consent_copy = self.cleaned_data.get('consent_copy')
        if consent_copy == NO:
            raise forms.ValidationError({
                'consent_copy':
                'Complete this part of the informed consent process'
                ' before continuing.'})

    def clean_consent_signature(self):
        consent_signature = self.cleaned_data.get('consent_signature')
        if consent_signature != YES:
            raise forms.ValidationError({
                'consent_signature':
                'Complete this part of the informed consent process'
                ' before continuing.'})
