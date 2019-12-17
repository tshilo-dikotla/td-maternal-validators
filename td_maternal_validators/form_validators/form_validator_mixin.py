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

    def validate_against_consent_datetime(self, report_datetime, id=None):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""

        consent = self.validate_against_consent(id=id)

        if report_datetime and report_datetime < consent.consent_datetime:
            raise forms.ValidationError(
                "Report datetime cannot be before consent datetime")

    def validate_against_consent(self, id=None):
        """Returns an instance of the current maternal consent version form or
        raises an exception if not found."""
        try:
            consent_version = self.consent_version_cls.objects.get(
                screening_identifier=self.subject_screening.screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Please complete mother\'s consent version form before proceeding')
        else:
            if not id:
                consent = self.maternal_consent_cls.objects.filter(
                    subject_identifier=self.subject_identifier,
                    version=consent_version.version).order_by(
                        '-consent_datetime').first()
            else:
                consent = self.maternal_consent_cls.objects.filter(
                    subject_identifier=self.subject_identifier).order_by(
                        'consent_datetime').first()
            if not consent:
                raise ValidationError(
                    'Please complete Maternal Consent form '
                    f'before  proceeding.')
            else:
                return consent

    @property
    def subject_screening(self):
        try:
            return self.subject_screening_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except self.subject_screening_cls.DoesNotExist:
            return None
