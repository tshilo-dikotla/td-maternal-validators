from django import forms
from django.apps import apps as django_apps
from edc_constants.constants import NEW, NO

from edc_action_item.site_action_items import site_action_items
from td_prn.action_items import MATERNALOFF_STUDY_ACTION
from td_prn.action_items import MATERNAL_DEATH_REPORT_ACTION


class TDCRFFormValidator:

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        if self.instance and not self.instance.id:
            self.validate_offstudy_model()
        super().clean()

    def validate_against_visit_datetime(self, report_datetime):
        if (report_datetime and report_datetime <
                self.cleaned_data.get('maternal_visit').report_datetime):
            raise forms.ValidationError(
                "Report datetime cannot be before visit datetime.")

    def validate_offstudy_model(self):
        maternal_offstudy_cls = django_apps.get_model(
            'td_prn.maternaloffstudy')
        action_cls = site_action_items.get(
            maternal_offstudy_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                action_type__name=MATERNALOFF_STUDY_ACTION,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            try:
                maternal_offstudy_cls.objects.get(
                    subject_identifier=self.subject_identifier)
            except maternal_offstudy_cls.DoesNotExist:
                pass
            else:
                raise forms.ValidationError(
                    'Participant has been taken offstudy. Cannot capture any '
                    'new data.')
        else:
            self.maternal_visit = self.cleaned_data.get('maternal_visit') or None
            if not self.maternal_visit or self.maternal_visit.require_crfs == NO:
                raise forms.ValidationError(
                    'Participant is scheduled to be taken offstudy without '
                    'any new data collection. Cannot capture any new data.')

    def validate_karabo_eligibility(self):
        karabo_screening_cls = django_apps.get_model(
            'td_maternal.karaboscreening')
        karabo_consent_cls = django_apps.get_model(
            'td_maternal.karaboconsent')
        try:
            karabo_screening_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except Exception:
            pass
