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
                self.required_if(
                    YES,
                    field='info_since_lastvisit',
                    field_required=required,
                )

        cleaned_data = self.cleaned_data
        if cleaned_data.get('value_vl') != 400 and cleaned_data.get('value_vl_size') \
                == 'less than':
            msg = {'value_vl': 'You indicated that the value of the most recent VL is'
                   'less_than a number,therefore the value of VL should be 400'}
            self._errors.update(msg)
            raise ValidationError(msg)

        cleaned_data = self.cleaned_data
        if cleaned_data.get('value_vl') != 750000 and cleaned_data.get('value_vl_size')\
                == 'greater than':
            msg = {'value_vl': 'You indicated that the value of the most recent VL is'
                   'less_than a number,therefore the value of VL should be 750000'}
            self._errors.update(msg)
            raise ValidationError(msg)

        cleaned_data = self.cleaned_data
        if cleaned_data.get('value_vl') != 750000 or cleaned_data.get('value_vl') != 400\
                and cleaned_data.get('value_vl_size') == 'equal':
            msg = {'You indicated that the value of the most recent VL is equal to a'
                   ' number, therefore the value of VL should be between 400 and 750000'
                   '(inclusive of 400 and 750,000)'
                   }
