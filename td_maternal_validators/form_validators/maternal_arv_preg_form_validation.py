from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .form_validator_mixin import TDFormValidatorMixin


class MaternalArvPregFormValidator(TDFormValidatorMixin, FormValidator):

    def clean(self):

        self.applicable_if(
            YES,
            field='is_interrupt',
            field_applicable='interrupt',
        )

        self.validate_other_specify(
            field='interrupt',
            other_specify_field='interrupt_other',
            required_msg='Please give reason for interruption'
        )
        qs = self.cleaned_data.get('maternal_arv_preg')
        print(qs)
