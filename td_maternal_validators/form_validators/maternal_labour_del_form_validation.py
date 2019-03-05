from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.utils import relativedelta
from edc_constants.constants import POS, YES, NOT_APPLICABLE, OTHER, NONE
from edc_form_validators import FormValidator
from td_maternal.helper_classes import MaternalStatusHelper

from .form_validator_mixin import TDFormValidatorMixin


class MaternalLabDelFormValidator(TDFormValidatorMixin, FormValidator):
    maternal_arv_model = 'td_maternal.maternalarv'
    maternal_visit_model = 'td_maternal.maternalvisit'

    @property
    def maternal_visit_cls(self):
        return django_apps.get_model(self.maternal_visit_model)

    @property
    def maternal_arv_cls(self):
        return django_apps.get_model(self.maternal_arv_model)

    def clean(self):
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))

        condition = self.cleaned_data.get(
            'mode_delivery') and 'c-section' in self.cleaned_data.get('mode_delivery')
        self.required_if_true(
            condition,
            field_required='csection_reason'
        )
        self.validate_initiation_date(cleaned_data=self.cleaned_data)
        self.validate_valid_regime_hiv_pos_only(cleaned_data=self.cleaned_data)
        self.validate_live_births_still_birth(cleaned_data=self.cleaned_data)
        self.validate_other()

    def validate_initiation_date(self, cleaned_data=None):
        subject_identifier = cleaned_data.get('subject_identifier')
        maternal_arv = self.maternal_arv_cls.objects.filter(
            maternal_arv_preg__maternal_visit__appointment__subject_identifier=subject_identifier,
            stop_date__isnull=True).order_by('-start_date').first()
        if maternal_arv:
            initiation_date = cleaned_data.get('arv_initiation_date')
            if initiation_date != maternal_arv.start_date:
                message = {'arv_initiation_date':
                           'ARV\'s initiation date must match start date '
                           'in pregnancy form, pregnancy form start date is '
                           f'{maternal_arv.start_date}, got {initiation_date}.'}
                self._errors.update(message)
                raise ValidationError(message)

    def validate_valid_regime_hiv_pos_only(self, cleaned_data=None):
        if self.maternal_status_helper.hiv_status == POS:
            if cleaned_data.get('valid_regiment_duration') != YES:
                message = {'valid_regiment_duration':
                           'Participant is HIV+ valid regimen duration '
                           'should be YES. Please correct.'}
                self._errors.update(message)
                raise ValidationError(message)
            self.required_if(
                YES,
                field='valid_regiment_duration',
                field_required='arv_initiation_date',
                required_msg='You indicated participant was on valid regimen, '
                'please give a valid arv initiation date.'
            )
            if (cleaned_data.get('valid_regiment_duration') == YES and
                (cleaned_data.get('delivery_datetime').date() - relativedelta(weeks=4) <
                 cleaned_data.get('arv_initiation_date'))):
                message = {'delivery_datetime':
                           'You indicated that the mother was on REGIMEN for a '
                           'valid duration, but delivery date is within 4weeks '
                           'of art initiation date. Please correct.'}
                self._errors.update(message)
                raise ValidationError(message)
        else:
            status = self.maternal_status_helper.hiv_status
            if cleaned_data.get('valid_regiment_duration') not in [NOT_APPLICABLE]:
                message = {'valid_regiment_duration':
                           f'Participant\'s HIV status is {status}, '
                           'valid regimen duration should be Not Applicable.'}
                self._errors.update(message)
                raise ValidationError(message)

            if cleaned_data.get('arv_initiation_date'):
                message = {'arv_initiation_date':
                           f'Participant\'s HIV status is {status}, '
                           'arv initiation date should not filled.'}
                self._errors.update(message)
                raise ValidationError(message)

    def validate_live_births_still_birth(self, cleaned_data=None):
        still_births = cleaned_data.get('still_births')
        live_births = cleaned_data.get('live_infants_to_register')
        if still_births == 0 and live_births != 1:
            message = {'live_infants_to_register':
                       'If still birth is 0 then live birth should be 1.'}
            self._errors.update(message)
            raise ValidationError(message)
        elif still_births == 1 and live_births != 0:
            message = {'still_births':
                       'If live births is 1 then still birth should be 0.'}
            self._errors.update(message)

    def validate_other(self):
        fields = {'delivery_hospital': 'delivery_hospital_other',
                  'mode_delivery': 'mode_delivery_other',
                  'csection_reason': 'csection_reason_other'}
        for field, other in fields.items():
            self.validate_other_specify(
                field=field,
                other_specify_field=other
            )
        selections = [OTHER, NONE]
        self.m2m_single_selection_if(
            *selections,
            m2m_field='delivery_complications')
        self.m2m_other_specify(
            OTHER,
            m2m_field='delivery_complications',
            field_other='delivery_complications_other')

    @property
    def maternal_status_helper(self):
        cleaned_data = self.cleaned_data
        latest_visit = self.maternal_visit_cls.objects.filter(
            subject_identifier=cleaned_data.get(
                'subject_identifier')).order_by('-created').first()
        if latest_visit:
            return MaternalStatusHelper(latest_visit)
        else:
            raise ValidationError(
                'Please complete previous visits before filling in '
                'Maternal Labour Delivery Form.')
