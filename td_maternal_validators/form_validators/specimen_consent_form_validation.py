from django import forms
from td_maternal.models import SubjectConsent
from edc_constants.constants import NO
from edc_form_validators import FormValidator


class SpecimenConsentFormValidator(FormValidator):

    STUDY_CONSENT = SubjectConsent

    def clean(self):

        self.required_if(
            NO,
            field='is_literate',
            field_required='witness_name',
            required_msg='You specified that participant is illiterate,'
            ' witness is required'
        )
        cleaned_data = super().clean()
        return cleaned_data

    def study_consent_or_raise(self):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""
        cleaned_data = self.cleaned_data
        subject_identifier = cleaned_data.get(
            'registered_subject').subject_identifier
        maternal_consent = self.STUDY_CONSENT.objects.filter(
            maternal_eligibility__registered_subject__subject_identifier=subject_identifier).order_by('consent_datetime').last()
        if not maternal_consent:
            raise forms.ValidationError(
                'Maternal consent must be completed before'
                ' the specimen consent.')

        return maternal_consent
