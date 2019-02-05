from django import forms


def validate_against_consent(self):
    """Returns an instance of the current maternal consent or
    raises an exception if not found."""
    cleaned_data = self.cleaned_data

    latest_consent = self.consent_model_cls.objects.filter(
        subject_identifier=self.cleaned_data.get('subject_identifier')
    ).order_by('-consent_datetime').first()

    if latest_consent:
        try:
            consent_version = self.consent_version_model.objects.get(
                screening_identifier=latest_consent.screening_identifier)
        except self.consent_version_model.DoesNotExist:
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
