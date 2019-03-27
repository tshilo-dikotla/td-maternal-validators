from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator


class MaternalTuberculosisHistoryFormValidator(TDCRFFormValidator,
                                               FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

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
