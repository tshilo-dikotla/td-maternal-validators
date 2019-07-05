from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator


class MaternalSubstanceUsePriorPregFormValidator(TDCRFFormValidator,
                                                 FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.required_if(
            YES,
            field='smoked_prior_to_preg',
            field_required='smoking_prior_preg_freq'
        )

        self.required_if(
            YES,
            field='alcohol_prior_pregnancy',
            field_required='alcohol_prior_preg_freq'
        )

        self.required_if(
            YES,
            field='marijuana_prior_preg',
            field_required='marijuana_prior_preg_freq'
        )
