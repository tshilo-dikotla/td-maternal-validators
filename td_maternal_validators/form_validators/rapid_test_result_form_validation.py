from edc_form_validators import FormValidator
from edc_constants.constants import YES


class RapidTestResultFormValidator(FormValidator):

    def clean(self):
        required_fields = ('result_date', 'result')
        for required in required_fields:
            self.required_if(
                YES,
                field='rapid_test_done',
                field_required=required,
                required_msg=('If a rapid test was processed, what is '
                              f'the {required} of the rapid test?'),
                not_required_msg=('If a rapid test was not processed, '
                                  f'please do not provide the {required}. '
                                  'Got {}.'.format(self.cleaned_data.get(required)))
            )
