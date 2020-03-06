from django import forms
from django.apps import apps as django_apps
from edc_action_item.site_action_items import site_action_items
from edc_constants.constants import NEW, NO
from td_prn.action_items import MATERNALOFF_STUDY_ACTION


class TDCRFFormValidator:

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()

    def validate_against_visit_datetime(self, report_datetime):
        if (report_datetime and report_datetime <
                self.cleaned_data.get('maternal_visit').report_datetime):
            raise forms.ValidationError(
                "Report datetime cannot be before visit datetime.")
