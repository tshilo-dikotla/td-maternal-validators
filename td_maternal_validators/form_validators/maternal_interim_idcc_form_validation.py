from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator


class MaternalIterimIdccFormValidator(TDCRFFormValidator,
                                      FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        required_fields = ['recent_cd4', 'recent_cd4_date', 'value_vl_size',
                           'value_vl', 'recent_vl_date']

        message = ('You indicated that there has not been any lab '
                   'information since the last visit please do not answer '
                   'the questions on CD4, VL.')

        for required in required_fields:
            if required in self.cleaned_data:
                self.not_required_if(
                    NO,
                    inverse=False,
                    field='info_since_lastvisit',
                    field_required=required,
                    not_required_msg=message
                )

        if self.cleaned_data.get('info_since_lastvisit') == YES:

            if (not self.cleaned_data.get('recent_cd4') and
                    not self.cleaned_data.get('value_vl_size')):
                msg = {'recent_cd4':
                       'New labs available, please add CD4 or Viral Load result'}
                self._errors.update(msg)
                raise ValidationError(msg)

            self.required_if_not_none(
                field='recent_cd4',
                field_required='recent_cd4_date')

            self.required_if_not_none(
                field='value_vl_size',
                field_required='value_vl')

            self.required_if_not_none(
                field='value_vl_size',
                field_required='recent_vl_date')

            self.validate_viral_load_value()

    def validate_viral_load_value(self):
        cleaned_data = self.cleaned_data
        vl_value = cleaned_data.get('value_vl')
        if cleaned_data.get('info_since_lastvisit') == YES and vl_value:
            if (vl_value != 400
                    and cleaned_data.get('value_vl_size') == 'less_than'):
                msg = {'value_vl': 'You indicated that the value of the most recent VL is '
                       f'less_than a {vl_value}, therefore the value of VL should be 400'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if (vl_value != 10000000
                    and cleaned_data.get('value_vl_size') == 'greater_than'):
                msg = {'value_vl': 'You indicated that the value of the most recent VL is '
                       f'greater_than a {vl_value}, therefore the value of VL should be 10,000,000'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if (vl_value > 10000000 or vl_value < 400
                    and cleaned_data.get('value_vl_size') == 'equal'):
                msg = {'value_vl': 'You indicated that the value of the '
                       f'most recent VL is equal to a {vl_value}, therefore the value of VL '
                       'should be between 400 and 10,000,000 (inclusive of 400 and 10,000,000)'}
                self._errors.update(msg)
                raise ValidationError(msg)
