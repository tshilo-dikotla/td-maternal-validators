from edc_constants.constants import YES
from edc_form_validators import FormValidator


class MaternalArvPregFormValidator(FormValidator):

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
