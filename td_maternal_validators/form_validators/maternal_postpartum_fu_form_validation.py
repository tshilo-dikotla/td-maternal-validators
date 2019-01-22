from django.core.exceptions import ValidationError
from edc_constants.constants import YES, POS, NOT_APPLICABLE, NO
from edc_form_validators import FormValidator
from td_maternal.helper_classes import MaternalStatusHelper


class MaternalPostPartumFuFormValidator(FormValidator):

    def clean(self):
        required_fields = ('hospitalization_reason', 'diagnoses')
        for required_field in required_fields:
            self.m2m_required(
                m2m_field=required_field
            )

        self.m2m_na_validation(
            field='new_diagnoses',
            m2m_field='diagnoses',
            msg=('Question4: Participant has new diagnoses, '
                 'list of diagnosis cannot be N/A'),
            na_msg=('Question4: Participant has no new diagnoses, '
                    'who listing should be N/A')
        )

        self.m2m_na_validation(
            field='hospitalized',
            m2m_field='hospitalization_reason',
            msg=('Question7: Participant was hospitalized, reasons cannot be N/A'),
            na_msg=('Question7: Participant was not hospitalized, '
                    'reasons should be N/A')
        )

        self.required_if(
            YES,
            field='hospitalized',
            field_required='hospitalization_days')

        if self.cleaned_data.get('hospitalized') == NO:
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field='hospitalization_reason')

        self.validate_who_diagnoses()

    def validate_who_diagnoses(self):
        condition = self.maternal_status_helper.hiv_status == POS
        self.applicable_if_true(
            condition,
            field_applicable='has_who_dx',
            applicable_msg='The mother is positive, question 10 for WHO '
                           'Stage III/IV should not be N/A',
            not_applicable_msg='The mother is Negative, question 10 for '
                               'WHO Stage III/IV should be N/A'
        )
        self.m2m_required(m2m_field='who')
        qs = self.cleaned_data.get('who').values_list(
            'short_name', flat=True)
        selection = list(qs.all())
        if not condition:
            if NOT_APPLICABLE not in selection:
                msg = {'who':
                       'The mother is Negative, WHO Stage III/IV listing '
                       'should be N/A'}
                self._errors.update(msg)
                raise ValidationError(msg)
            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field='who')
        if condition:
            self.m2m_na_validation(
                field='has_who_dx',
                m2m_field='who',
                msg='Question 11 is indicated as YES, who listing cannot be N/A',
                na_msg='Question 11 is indicated as NO, who listing should be N/A')

    def m2m_na_validation(self, field=None, m2m_field=None, msg=None,
                          na_msg=None):
        qs = self.cleaned_data.get(m2m_field).values_list(
            'short_name', flat=True)
        selection = list(qs.all())
        if self.cleaned_data.get(field) == YES:
            if NOT_APPLICABLE in selection:
                message = {m2m_field: msg}
                self._errors.update(message)
                raise ValidationError(message)
        else:
            if NOT_APPLICABLE not in selection:
                message = {m2m_field: na_msg}
                self._errors.update(message)
                raise ValidationError(message)

            self.m2m_single_selection_if(
                NOT_APPLICABLE,
                m2m_field=m2m_field
            )

    @property
    def maternal_status_helper(self):
        cleaned_data = self.cleaned_data
        return MaternalStatusHelper(cleaned_data.get('maternal_visit'))
