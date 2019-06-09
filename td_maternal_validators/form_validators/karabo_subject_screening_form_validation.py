from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator


class KaraboSubjectScreeningFormValidator(TDCRFFormValidator, FormValidator):

    infant_birth_model = 'td_infant.infantbirth'

    @property
    def infant_birth_cls(self):
        return django_apps.get_model(self.infant_birth_model)

    def clean(self):
        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get('subject_identifier') + '-10'
        self.validate_against_birth_date(
            infant_identifier=self.subject_identifier,
            report_datetime=cleaned_data.get('report_datetime'))
        super().clean()

    def validate_against_birth_date(self, infant_identifier=None,
                                    report_datetime=None):

        try:
            infant_birth = self.infant_birth_cls.objects.get(
                subject_identifier=infant_identifier)
        except self.infant_birth_cls.DoesNotExist:
            raise ValidationError(
                'Please complete Infant Birth form '
                f'before  proceeding.')
        else:
            if report_datetime and report_datetime < infant_birth.report_datetime:
                raise forms.ValidationError(
                    "Report datetime cannot be before infant birth datetime.")
            else:
                return infant_birth
