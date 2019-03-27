from django.apps import apps as django_apps
from django.forms import forms
from edc_constants.constants import NO
from edc_form_validators import FormValidator

from ..constants import NEVER_STARTED
from .crf_form_validator import TDCRFFormValidator


class MarternalArvPostFormValidator(TDCRFFormValidator,
                                    FormValidator):

    maternal_arv_post_adh = 'td_maternal.maternalarvpostadh'

    @property
    def maternal_arv_post_adh_cls(self):
        return django_apps.get_model(self.maternal_arv_post_adh)

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        condition = (self.cleaned_data.get('on_arv_since') == NO
                     or self.cleaned_data.get('arv_status') == NEVER_STARTED)
        if condition:
            maternal_arv_post_adh = self.maternal_arv_post_adh_cls.objects.filter(
                maternal_visit=self.cleaned_data.get('maternal_visit'))
            if maternal_arv_post_adh:
                msg = {'ARV history exists. You wrote mother did NOT receive ARVs '
                       'in this pregnancy. Please correct '
                       f'{self.maternal_arv_post_adh_cls._meta.verbose_name} first'
                       }
                raise forms.ValidationError(msg)
            else:
                pass

        self.not_applicable_if(
            NO,
            field='on_arv_since',
            field_applicable='on_arv_reason')

        self.validate_other_specify(
            field='on_arv_reason',
            other_specify_field='on_arv_reason_other',
        )
