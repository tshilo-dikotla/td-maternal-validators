from django import forms
from django.apps import apps as django_apps
from edc_action_item.site_action_items import site_action_items
from edc_constants.constants import NEW

from td_maternal.action_items import MATERNALOFF_STUDY_ACTION
from td_maternal.action_items import MATERNAL_DEATH_REPORT_ACTION


class TDCRFFormValidator:

    def clean(self):
        if self.instance and not self.instance.id:
            self.validate_offstudy_model()
        super().clean()

    def validate_offstudy_model(self):
        maternal_offstudy_cls = django_apps.get_model(
            'td_maternal.maternaloffstudy')
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
            raise forms.ValidationError(
                'Participant is scheduled to be taken offstudy. Cannot capture '
                'any new data.')
