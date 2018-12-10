from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator


class AntenatalVisitMembershipFormValidator(FormValidator):

    consent_version_model = 'td_maternal.tdconsentversion'

    maternal_consent_model = 'td_maternal.subjectconsent'

    @property
    def consent_version_cls(self):
        return django_apps.get_model(self.consent_version_model)

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_consent_model)

    def clean(self):
        self.validate_current_consent_version(cleaned_data=self.cleaned_data)

    def validate_current_consent_version(self, cleaned_data=None):
        try:
            td_consent_version = self.consent_version_cls.objects.get(
                subjectscreening=cleaned_data.get('subjectscreening'))
        except self.consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Complete mother\'s consent version form before proceeding')
        else:
            try:
                self.maternal_consent_cls.objects.get(
                    screening_identifier=cleaned_data.get(
                        'subjectscreening').screening_identifier,
                    version=td_consent_version.version)
            except self.maternal_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Maternal Consent form for version {} before '
                    'proceeding'.format(td_consent_version.version))
