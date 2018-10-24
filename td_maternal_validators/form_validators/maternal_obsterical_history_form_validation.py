from django.core.exceptions import ValidationError
from edc_form_validators.form_validator import FormValidator


class MaternalObstericalHistoryFormValidator(FormValidator):
    def clean(self):

        if not self.cleaned_data.get('ultrasound'):
            message = {'ultrasound': 'Please complete ultrasound form first'}
            self._errors.update(message)
            raise ValidationError(message)

        ultrasound = self.cleaned_data.get('ultrasound')
        if (self.cleaned_data.get('prev_pregnancies') == 1 and
                ultrasound[0].ga_confirmed < 24):
            fields = ['pregs_24wks_or_more',
                      'lost_before_24wks', 'lost_after_24wks']
            for field in fields:
                if (field in self.cleaned_data and
                        self.cleaned_data.get(field) != 0):
                    message = {field: 'You indicated previous pregnancies were'
                                      ' %s, %s should be zero' %
                               (self.cleaned_data.get('prev_pregnancies'),
                                field)}
                    self._errors.update(message)
                    raise ValidationError(message)

        if ('prev_pregnancies' in self.cleaned_data and
                self.cleaned_data.get('prev_pregnancies') > 0):
            sum_pregs = (self.cleaned_data.get('pregs_24wks_or_more') +
                         (self.cleaned_data.get('lost_before_24wks')))

            previous_pregs = (self.cleaned_data.get('prev_pregnancies'))

            if (sum_pregs != previous_pregs):
                raise ValidationError('Total pregnancies should be '
                                      'equal to sum of pregancies '
                                      'lost and current')

            if (self.cleaned_data.get('pregs_24wks_or_more') <
                    self.cleaned_data.get('lost_after_24wks')):
                message = {'pregs_24wks_or_more':
                           'Sum of Pregnancies more than'
                           '24 weekss should be '
                           'less than those lost'}
                self._errors.update(message)
                raise ValidationError(message)

        if self.cleaned_data.get('children_deliv_before_37wks'):
            cleaned_data = self.cleaned_data
            sum_deliv_37_wks = \
                (cleaned_data.get('children_deliv_before_37wks') +
                 cleaned_data.get('children_deliv_aftr_37wks'))
            sum_lost_24_wks = (cleaned_data.get('lost_before_24wks') +
                               cleaned_data.get('lost_after_24wks'))
            if sum_deliv_37_wks != ((cleaned_data.get('prev_pregnancies') - 1)
                                    - sum_lost_24_wks):
                raise ValidationError('The sum of Q8 and Q9 must be equal to '
                                      '(Q2 -1) - (Q4 + Q5). Please correct.')
