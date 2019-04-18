from django.core.exceptions import ValidationError
from edc_constants.constants import NO, YES, DWTA, OTHER
from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator


class MaternalSrhFormValidator(TDCRFFormValidator,
                               FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.not_required_if(
            YES,
            field='seen_at_clinic',
            field_required='reason_unseen_clinic',
            required_msg=('If you have not been seen in that clinic since '
                          'your last visit with us, why not?')
        )
        self.validate_other_specify(
            field='reason_unseen_clinic',
            other_specify_field='reason_unseen_clinic_other',
            other_stored_value=OTHER)

        condition = not(self.cleaned_data.get('reason_unseen_clinic') == None)
        self.required_if_true(
            condition,
            field_required='reason_unseen_clinic_other'
        )

        self.required_if(
            YES,
            field='seen_at_clinic',
            field_required='is_contraceptive_initiated')

        self.m2m_required_if(
            YES,
            field='is_contraceptive_initiated',
            m2m_field='contr')

        self.m2m_other_specify(
            m2m_field='contr',
            field_other='contr_other'
        )
        self.required_if(
            YES,
            field='is_contraceptive_initiated',
            field_required='reason_not_initiated'
        )

        self.validate_other_specify(
            field='reason_not_initiated',
            other_specify_field='reason_not_initiated_other',
            other_stored_value=OTHER)

        self.validate_seen_at_clinic_DWTA(cleaned_data=self.cleaned_data)
        self.validate_not_tried(cleaned_data=self.cleaned_data)

    def validate_seen_at_clinic_DWTA(self, cleaned_data=None):
        if cleaned_data.get('seen_at_clinic') == DWTA:
            if (cleaned_data.get('reason_unseen_clinic') or
                cleaned_data.get('is_contraceptive_initiated') or
                cleaned_data.get('contr') or
                    cleaned_data.get('reason_not_initiated')):
                msg = {'reason_not_initiated':
                       'If participant does not want to answer, the questionnaire is complete.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_not_tried(self, cleaned_data=None):
        if cleaned_data.get('reason_unseen_clinic') == 'not_tried':
            if (cleaned_data.get('is_contraceptive_initiated') or
                cleaned_data.get('contr') or
                    cleaned_data.get('reason_not_initiated')):
                msg = {'reason_unseen_clinic':
                       'If Q3 is \'No\' all Questions after Question 4 '
                       'must be None or Blank.'}
                self._errors.update(msg)
                raise ValidationError(msg)
