from django.core.exceptions import ValidationError
from edc_constants.constants import (YES, NO, RESTARTED, CONTINUOUS, STOPPED)
from edc_form_validators import FormValidator


class MaternalLifetimeArvHistoryFormValidator(FormValidator):

    def clean(self):
        responses = [RESTARTED, CONTINUOUS]
        for response in responses:
            if (self.cleaned_data.get('preg_on_haart') == NO
                    and response in self.cleaned_data.get('prior_preg')):
                msg = {'prior_preg': 'You indicated that the mother was NOT on'
                       ' triple ARV when she got pregnant. Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)

        if (self.cleaned_data.get('preg_on_haart') == YES
                and self.cleaned_data.get('prior_preg') == STOPPED):
            msg = {'prior_preg': 'You indicated that the mother was still on '
                                 'triple ARV when she got pregnant, yet you '
                                 'indicated that ARVs were interrupted and '
                                 'never restarted. Please correct.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        self.required_if(
            YES,
            field='preg_on_haart',
            field_required='haart_start_date',
            required_msg='The subject has received haart when pregnant, '
                         'please provide the date it was first started.')

        self.required_if_not_none(
            field='haart_start_date',
            field_required='is_date_estimated',
            required_msg='Please answer: Is the subject\'s date of triple'
                         ' antiretrovirals estimated?')

        self.required_if(
            YES,
            field='prev_preg_haart',
            field_required='haart_start_date',
            required_msg='Please give date triple antiretrovirals '
            'first started.'
        )
