from django import forms
from django.apps import apps as django_apps
from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator


class SpecimenConsentFormValidator(FormValidator):

    consent_cls = 'td_maternal.subjectconsent'
    consent_version_cls = 'td_maternal.tdconsentversion'

    consent_model_cls = django_apps.get_model(consent_cls)
    consent_version_model = django_apps.get_model(consent_version_cls)

    def clean(self):

        self.required_if(
            NO,
            field='is_literate',
            field_required='witness_name',
            required_msg='You specified that participant is illiterate,'
            ' witness is required'
        )

        study_consent = self.validate_against_consent()
        self.compare_attr_to_study_consent('is_literate', study_consent)
        self.compare_attr_to_study_consent('witness_name', study_consent)
        self.purpose_explained_and_understood()
        self.copy_of_consent_provided()

    def validate_against_consent(self):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""
        latest_consent = self.consent_model_cls.objects.filter(
            subject_identifier=self.cleaned_data.get('subject_identifier')
        ).order_by('-consent_datetime').first()

        if latest_consent:
            try:
                consent_version = self.consent_version_model.objects.get(
                    screening_identifier=latest_consent.screening_identifier)
            except self.consent_version_model.DoesNotExist:
                raise forms.ValidationError(
                    'Subject consent version form must be completed before'
                    ' the specimen consent.')

        if (not latest_consent
                or latest_consent.version != consent_version.version):
            raise forms.ValidationError(
                'Subject consent must be completed before'
                ' the specimen consent.')
        return latest_consent

    def compare_attr_to_study_consent(self, attrname, study_consent):
        """Compares the value of a specimen consent attribute to that on the
        study consent and raises if the values are not equal."""
        cleaned_data = self.cleaned_data
        value = cleaned_data.get(attrname)
        study_consent_value = getattr(study_consent, attrname)
        if value != study_consent_value:
            fields = [
                field for field in study_consent._meta.fields
                if field.name == attrname]
            question = ', '.join([fld.verbose_name for fld in fields])
            raise forms.ValidationError(
                {question: 'Specimen consent and maternal consent do not match'
                 f' for question \'{question}\'. Got {value} !='
                 f' {study_consent_value}. Please correct.'})

    def purpose_explained_and_understood(self):
        """Ensures the purpose of specimen storage is indicated as
        explained and understood."""
        cleaned_data = self.cleaned_data
        if cleaned_data.get("may_store_samples") == YES:
            if cleaned_data.get("purpose_explained") != YES:
                raise forms.ValidationError(
                    {'purpose_explained':
                     "If the participant agrees for specimens to be stored, "
                     "ensure that purpose of specimen storage is explained."})
            if cleaned_data.get("purpose_understood") != YES:
                raise forms.ValidationError(
                    {'purpose_understood':
                     "If the participant agrees for specimens to be stored, "
                     "ensure that participant understands the purpose,  "
                     "procedures and benefits of specimen storage."})

    def copy_of_consent_provided(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("may_store_samples") == NO:
            if cleaned_data.get('offered_copy') != NO:
                raise forms.ValidationError(
                    {'offered_copy':
                     'Participant did not agree for specimens to be stored. '
                     'Do not provide the participant with a copy of the '
                     'specimen consent.'})
