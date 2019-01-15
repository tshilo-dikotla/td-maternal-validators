from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import (YES, NO, RESTARTED, CONTINUOUS, STOPPED)
from edc_form_validators import FormValidator


class MaternalLifetimeArvHistoryFormValidator(FormValidator):
    maternal_consent_model = 'td_maternal.subjectconsent'
    ob_history_model = 'td_maternal.maternalobstericalhistory'

    @property
    def maternal_consent_model_cls(self):
        return django_apps.get_model(self.maternal_consent_model)

    @property
    def maternal_ob_history_model_cls(self):
        return django_apps.get_model(self.ob_history_model)

    def clean(self):
        self.required_if(
            YES,
            field='prev_preg_haart',
            field_required='haart_start_date',
            required_msg='The subject has received haart when pregnant, '
                         'please provide the date it was first started.')

        self.required_if_not_none(
            field='haart_start_date',
            field_required='is_date_estimated',
            required_msg='Please answer: Is the subject\'s date of triple'
                         ' antiretrovirals estimated?')

        self.validate_prior_preg(cleaned_data=self.cleaned_data)

        self.validate_maternal_consent(cleaned_data=self.cleaned_data)

        self.validate_prev_preg(cleaned_data=self.cleaned_data)

    def validate_prior_preg(self, cleaned_data=None):
        responses = (CONTINUOUS, RESTARTED)
        if (cleaned_data.get('preg_on_haart') == NO
                and self.cleaned_data.get('prior_preg') in responses):
            msg = {'prior_preg': 'You indicated that the mother was NOT on'
                   ' triple ARV when she got pregnant. Please correct.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if (cleaned_data.get('preg_on_haart') == YES
                and self.cleaned_data.get('prior_preg') == STOPPED):
            msg = {'prior_preg': 'You indicated that the mother was still on '
                                 'triple ARV when she got pregnant, yet you '
                                 'indicated that ARVs were interrupted and '
                                 'never restarted. Please correct.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_maternal_consent(self, cleaned_data=None):
        if cleaned_data.get('haart_start_date'):
            try:
                maternal_consent = self.maternal_consent_model_cls.objects.get(
                    subject_identifier=cleaned_data.get(
                        'maternal_visit').appointment.subject_identifier)
                if cleaned_data.get('report_datetime') < maternal_consent.consent_datetime:
                    msg = {'report_datetime': 'Report datetime CANNOT be '
                                              'before consent datetime'}
                    self._errors.update(msg)
                    raise ValidationError(msg)

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
                if cleaned_data.get('haart_start_date') < maternal_consent.dob:
                    msg = {'haart_start_date': 'Date of triple ARVs first '
                                               'started CANNOT be before DOB.'}
                    self._errors.update(msg)
                    raise ValidationError(msg)
            except self.maternal_consent_model_cls.DoesNotExist:
                raise ValidationError('Maternal Consent does not exist.')

    def validate_prev_preg(self, cleaned_data=None):
        ob_history = self.maternal_ob_history_model_cls.objects.filter(
            maternal_visit__appointment__subject_identifier=cleaned_data.get(
                'maternal_visit').appointment.subject_identifier)
        if not ob_history:
            raise ValidationError(
                'Please fill in the Maternal Obsterical History form first.')
        else:
            condition = ob_history[0].prev_pregnancies != 0
            fields_applicable = ['prev_preg_azt',
                                 'prev_sdnvp_labour', 'prev_preg_haart']
            for field_applicable in fields_applicable:
                self.applicable_if_true(
                    condition=condition,
                    field_applicable=field_applicable,
                )
