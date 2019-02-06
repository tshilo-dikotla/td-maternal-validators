from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator


class AntenatalVisitMembershipFormValidator(FormValidator):

    consent_version_model = 'td_maternal.tdconsentversion'

    maternal_consent_model = 'td_maternal.subjectconsent'

    subject_screening_model = 'td_maternal.subjectscreening'

    @property
    def consent_version_cls(self):
        return django_apps.get_model(self.consent_version_model)

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_consent_model)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    def clean(self):
        self.validate_current_consent_version()
        self.validate_against_consent()

    def validate_current_consent_version(self):
        try:
            td_consent_version = self.consent_version_cls.objects.get(
                screening_identifier=self.subject_screening.screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Complete mother\'s consent version form before proceeding')
        else:
            try:
                self.maternal_consent_cls.objects.get(
                    subject_identifier=self.cleaned_data.get(
                        'subject_identifier'),
                    version=td_consent_version.version)
            except self.maternal_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Maternal Consent form for version '
                    f'{td_consent_version.version} before proceeding.')

    def validate_against_consent(self):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""
        cleaned_data = self.cleaned_data

        latest_consent = self.maternal_consent_cls.objects.filter(
            subject_identifier=self.cleaned_data.get('subject_identifier')
        ).order_by('-consent_datetime').first()

        if latest_consent:
            try:
                consent_version = self.consent_version_cls.objects.get(
                    screening_identifier=latest_consent.screening_identifier)
            except self.consent_version_cls.DoesNotExist:
                raise forms.ValidationError(
                    'Subject consent version form must be completed first.')

            if cleaned_data.get("report_datetime") < latest_consent.consent_datetime:
                raise forms.ValidationError(
                    "Report datetime cannot be before consent datetime")

        if (not latest_consent
                or latest_consent.version != consent_version.version):
            raise forms.ValidationError(
                'Subject consent must be completed before first.')
        return latest_consent

    @property
    def subject_screening(self):
        cleaned_data = self.cleaned_data
        try:
            return self.subject_screening_cls.objects.get(
                subject_identifier=cleaned_data.get('subject_identifier'))
        except self.subject_screening_cls.DoesNotExist:
            return None
