from edc_constants.constants import NO
from edc_form_validators import FormValidator


class MaternalRecontactFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            NO,
            field='future_contact',
            field_required='reason_no_contact',
        )
