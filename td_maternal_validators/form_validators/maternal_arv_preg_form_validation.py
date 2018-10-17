from edc_constants.constants import YES
from edc_form_validators import FormValidator


class MaternalArvPregFormValidator(FormValidator):

    def clean(self):
        self.applicable_if(
            YES,
            field='is_interrupt',
            field_applicable='interrupt',
        )
