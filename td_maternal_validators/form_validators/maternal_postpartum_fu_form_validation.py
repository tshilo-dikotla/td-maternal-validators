from edc_constants.constants import YES, NEG
from edc_form_validators import FormValidator


class MaternalPostPartumFuFormValidator(FormValidator):

    def clean(self):
        required_fields = ['hospitalization_reason', 'diagnoses']
        for required in required_fields:
            self.m2m_required(required)

        self.required_if(
            YES,
            field='hospitalized',
            field_required='hospitalization_days')

        m2m_fields = {'hospitalized': 'hospitalization_reason',
                      'new_diagnoses': 'diagnoses'}
        for k, v in m2m_fields.items():
            self.m2m_validate_not_applicable(
                YES,
                field=k,
                m2m_field=v)

        self.not_applicable(
            NEG,
            field='subject_status',
            field_applicable='has_who_dx')
