from django.core.exceptions import ValidationError
from edc_constants.constants import NO, YES, DWTA, OTHER, NOT_APPLICABLE
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

        condition = self.cleaned_data.get('reason_unseen_clinic') == OTHER
        self.required_if_true(
            condition,
            field_required='reason_unseen_clinic_other'
        )

        self.required_if(
            YES,
            field='seen_at_clinic',
            field_required='is_contraceptive_initiated')

        self.m2m_other_specify(
            OTHER,
            m2m_field='contr',
            field_other='contr_other'
        )
        self.required_if(
            NO,
            field='is_contraceptive_initiated',
            field_required='reason_not_initiated'
        )

        self.validate_other_specify(
            field='reason_not_initiated',
            other_specify_field='reason_not_initiated_other',
            other_stored_value=OTHER)

        self.validate_seen_at_clinic_DWTA(cleaned_data=self.cleaned_data)
        self.validate_not_tried(cleaned_data=self.cleaned_data)
        self.validate_m2m_required()
        self.validate_m2m_required_()

    def validate_seen_at_clinic_DWTA(self, cleaned_data=None):
        if cleaned_data.get('seen_at_clinic') == DWTA:
            if (cleaned_data.get('reason_unseen_clinic') or
                cleaned_data.get('is_contraceptive_initiated') or
                cleaned_data.get('contr') or
                    cleaned_data.get('reason_not_initiated')):
                msg = {'reason_not_initiated':
                       'If participant does not want to answer,'
                       ' the questionnaire is complete.'}
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

    def validate_m2m_required(self):
        qs = self.cleaned_data.get('contr')
        if qs and qs.count() >= 1:
            selected = {obj.short_name: obj.name for obj in qs}
            if (self.cleaned_data.get('is_contraceptive_initiated') == YES and
                    NOT_APPLICABLE in selected):
                message = {
                    'contr':
                    'This field is applicable.'}
                raise ValidationError(message)

    def validate_m2m_required_(self):
        is_contraceptive_initiated = self.cleaned_data.get('is_contraceptive_initiated')
        qs = self.cleaned_data.get('contr')

        if qs and qs.count() >= 1:
            selected = {obj.short_name: obj.name for obj in qs}
            if not is_contraceptive_initiated == YES \
                    and (NOT_APPLICABLE not in selected):
                        message = {
                            'contr':
                            'Answer should be Not Applicable for this field'
                        }
                        raise ValidationError(message)

            if (is_contraceptive_initiated == YES and \
                    NOT_APPLICABLE in selected):
                        message = {
                            'contr':
                            'This field cannot be Not Applicable.'}
                        raise ValidationError(message)
        elif qs.count() < 1:
                message = {
                    'contr':
                    'This field is required.'
                }
                raise ValidationError(message)
