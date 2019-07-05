from django import forms
from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator
from .form_validator_mixin import TDFormValidatorMixin


class SpecimenConsentFormValidator(TDCRFFormValidator,
                                   TDFormValidatorMixin, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        if self.instance and not self.instance.id:
            self.validate_offstudy_model()

        self.required_if(
            NO,
            field='is_literate',
            field_required='witness_name',
            required_msg='You specified that participant is illiterate,'
            ' witness is required'
        )

        self.validate_against_consent_datetime(
            self.cleaned_data.get('consent_datetime'))
        study_consent = self.validate_against_consent()
        self.compare_attr_to_study_consent('is_literate', study_consent)
        self.compare_attr_to_study_consent('witness_name', study_consent)
        self.consent_reviewed_and_assessment_score()
        self.copy_of_consent_provided()

    def compare_attr_to_study_consent(self, attrname, study_consent):
        '''Compares the value of a specimen consent attribute to that on the
        study consent and raises if the values are not equal.'''
        cleaned_data = self.cleaned_data
        value = cleaned_data.get(attrname)
        study_consent_value = getattr(study_consent, attrname)
        if value != study_consent_value:
            fields = [
                field for field in study_consent._meta.fields
                if field.name == attrname]
            question = ', '.join([fld.verbose_name for fld in fields])
            raise forms.ValidationError(
                {attrname: 'Specimen consent and maternal consent do not match'
                 f' for question \'{question}\'. Got {value} !='
                 f' {study_consent_value}. Please correct.'})

    def consent_reviewed_and_assessment_score(self):
        '''Ensures the purpose of specimen storage is indicated as
        explained and understood.'''
        cleaned_data = self.cleaned_data
        if cleaned_data.get('may_store_samples') == YES:
            if cleaned_data.get('consent_reviewed') != YES:
                raise forms.ValidationError(
                    {'consent_reviewed':
                     'If the participant agrees for specimens to be stored, '
                     'ensure that purpose of specimen storage is explained.'})
            if cleaned_data.get('assessment_score') != YES:
                raise forms.ValidationError(
                    {'assessment_score':
                     'If the participant agrees for specimens to be stored, '
                     'ensure that participant understands the purpose,  '
                     'procedures and benefits of specimen storage.'})

    def copy_of_consent_provided(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('may_store_samples') == NO
                and cleaned_data.get('consent_copy') != NO):
            raise forms.ValidationError(
                {'consent_copy':
                 'Participant did not agree for specimens to be stored. '
                 'Do not provide the participant with a copy of the '
                 'specimen consent.'})
        elif (self.cleaned_data.get('may_store_samples') == YES and
                self.cleaned_data.get('consent_copy') == NO):
            raise forms.ValidationError(
                {'consent_copy':
                 'Please provide the subject with a copy of the consent.'})
