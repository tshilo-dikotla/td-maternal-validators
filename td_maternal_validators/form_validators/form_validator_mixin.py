from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError


class TDFormValidatorMixin:

    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'
    consent_version_model = 'td_maternal.tdconsentversion'
    maternal_consent_model = 'td_maternal.subjectconsent'
    subject_screening_model = 'td_maternal.subjectscreening'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    @property
    def consent_version_cls(self):
        return django_apps.get_model(self.consent_version_model)

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_consent_model)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    def validate_against_consent_datetime(self, report_datetime):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""

        latest_consent = self.validate_against_consent()
        if report_datetime and report_datetime < latest_consent.consent_datetime:
            raise forms.ValidationError(
                "Report datetime cannot be before consent datetime")

    def validate_against_consent(self):
        """Returns an instance of the current maternal consent version form or
        raises an exception if not found."""
        try:
            self.consent_version_cls.objects.get(
                screening_identifier=self.subject_screening.screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Please complete mother\'s consent version form before proceeding')
        else:
            try:
                latest_consent = self.maternal_consent_cls.objects.get(
                    subject_identifier=self.cleaned_data.get('subject_identifier'))
            except self.maternal_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Please complete Maternal Consent form '
                    f'before  proceeding.')
            else:
                return latest_consent

    @property
    def subject_screening(self):
        cleaned_data = self.cleaned_data
        try:
            return self.subject_screening_cls.objects.get(
                subject_identifier=cleaned_data.get('subject_identifier'))
        except self.subject_screening_cls.DoesNotExist:
            return None
