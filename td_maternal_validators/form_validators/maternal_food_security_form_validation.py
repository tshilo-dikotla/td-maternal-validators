from edc_constants.constants import YES
from edc_form_validators.form_validator import FormValidator

from .crf_form_validator import TDCRFFormValidator


class MaternalFoodSeccurityFormValidator(TDCRFFormValidator, FormValidator):

    def clean(self):

        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.required_if(
            YES,
            field='skip_meals',
            field_required='skip_meals_frequency')
