from edc_constants.constants import YES
from edc_form_validators import FormValidator


class MaternalPostPartumFuFormValidator(FormValidator):

    def clean(self):
        self.m2m_required_if(
            YES,
            field='hospitalized',
            m2m_field='hospitalization_reason')

        self.required_if(
            YES,
            field='hospitalized',
            field_required='hospitalization_days')
