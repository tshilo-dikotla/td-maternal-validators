from edc_form_validators import FormValidator


class MaternalDemographicsFormValidator(FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='marital_status',
        )

        self.validate_other_specify(
            field='ethnicity',
        )

        self.validate_other_specify(
            field='current_occupation',
        )

        self.validate_other_specify(
            field='provides_money',
        )

        self.validate_other_specify(
            field='money_earned',
        )
