from edc_form_validators import FormValidator
from edc_constants.constants import YES


class MaternalTuberculosisHistoryFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='coughing',
            field_required='coughing_rel'
        ),

        self.required_if(
            YES,
            field='diagnosis',
            field_required='diagnosis_rel'
        ),

        self.required_if(
            YES,
            field='tb_treatment',
            field_required='tb_treatment_rel'
        )
