from edc_constants.constants import YES
from edc_form_validators import FormValidator
from django.core.exceptions import ValidationError


class MaternalIterimIdccFormValidator(FormValidator):
    def clean(self):
        required_fields = ['recent_cd4', 'recent_cd4_date']
        for required in required_fields:
            if required in self.cleaned_data:
                self.required_if(
                    YES,
                    field='info_since_lastvisit',
                    field_required=required,
                )

        required_fields = ['value_vl', 'recent_vl_date']
        for required in required_fields:
            if required in self.cleaned_data:
                self.required_if_not_none(
                    field='value_vl_size',
                    field_required=required)
        self.validate_viral_load_value()

    def validate_viral_load_value(self):
        cleaned_data = self.cleaned_data
        vl_value = cleaned_data.get('value_vl')
        if vl_value:
            if (vl_value != 400
                    and cleaned_data.get('value_vl_size') == 'less_than'):
                msg = {'value_vl': 'You indicated that the value of the most recent VL is '
                       f'less_than a {vl_value}, therefore the value of VL should be 400'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if (vl_value != 750000
                    and cleaned_data.get('value_vl_size') == 'greater_than'):
                msg = {'value_vl': 'You indicated that the value of the most recent VL is '
                       f'greater_than a {vl_value}, therefore the value of VL should be 750000'}
                self._errors.update(msg)
                raise ValidationError(msg)

            if (vl_value > 750000 or vl_value < 400
                    and cleaned_data.get('value_vl_size') == 'equal'):
                msg = {'value_vl': 'You indicated that the value of the '
                       f'most recent VL is equal to a {vl_value}, therefore the value of VL '
                       'should be between 400 and 750000 (inclusive of 400 and 750,000)'}
                self._errors.update(msg)
                raise ValidationError(msg)
