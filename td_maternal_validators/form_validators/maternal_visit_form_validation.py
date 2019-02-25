from edc_form_validators import FormValidator
from edc_visit_tracking.form_validators import VisitFormValidator


class MaternalVisitFormValidator(VisitFormValidator, FormValidator):

    def clean(self):
        print(self.cleaned_data['survival_status'])
        condition = True if self.cleaned_data['survival_status'] == 'alive' \
            or self.cleaned_data['survival_status'] == 'dead' else False
        self.required_if_true(
            condition=condition,
            field_required='last_alive_date'
        )
        VisitFormValidator.clean(self)
