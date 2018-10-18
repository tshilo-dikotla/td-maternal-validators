from edc_constants.constants import YES
from edc_form_validators import FormValidator


class MaternalLifetimeArvHistoryFormValidator(FormValidator):
    maternal_ob_history_cls = 'td_maternal.maternalobstericalhistory'

    def clean(self):

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

        maternal_ob_history_cls = self.maternal_ob_history_cls.objects.filter(
            maternal_visit__appointment__subject_identifier=self.cleaned_data.
            get('maternal_visit').appointment.subject_identifier)
