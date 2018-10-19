from django.forms import forms
from edc_constants.constants import NO
from edc_form_validators import FormValidator

from ..constants import NEVER_STARTED


class MarternalArvPostFormValidator(FormValidator):

    maternal_arv_post_adh = 'td_maternal.maternalarvpostadh'

    def clean(self):

        condition = (self.cleaned_data.get('on_arv_since') == NO or
                     self.cleaned_data.get('arv_status') == NEVER_STARTED)
        if condition:
            if self.maternal_arv_post_adh_cls.objects.filter(maternal_visit=self.cleaned_data.get('maternal_visit')):

                msg = {"ARV history exists. You wrote mother did NOT receive ARVs "
                       f"in this pregnancy. Please correct '{self.maternal_arv_post_adh._meta.verbose_name}' first."
                       }
                self._errors.update(msg)
                raise forms.ValidationError(msg)
