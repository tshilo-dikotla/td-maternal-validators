from edc_form_validators import FormValidator
from edc_constants.constants import YES, NO

from ..constants import RESTARTED


class MaternalArvHistoryFormValidator(FormValidator):

    def clean(self):

        condition = (
            self.cleaned_data.get('preg_on_haart') == NO and
            self.cleaned_data.get('prior_preg') == RESTARTED)
        self.not_required_if(
            condition=condition,
            field='prev_preg_azt',
            field_required='prior_preg')
