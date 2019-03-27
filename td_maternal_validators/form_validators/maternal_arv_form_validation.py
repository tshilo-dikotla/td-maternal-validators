from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import TDCRFFormValidator


class MaternalArvFormValidator(TDCRFFormValidator,
                               FormValidator):

    arv_history_model = 'td_maternal.maternallifetimearvhistory'

    @property
    def arv_history_cls(self):
        return django_apps.get_model(self.arv_history_model)

    def clean(self):
        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        self.validate_date(cleaned_data=self.cleaned_data)
        self.validate_took_arv(cleaned_data=self.cleaned_data)
        self.validate_historical_and_present_arv_start_dates(
            cleaned_data=self.cleaned_data)
        self.validate_reason_for_stop()

    def validate_date(self, cleaned_data=None):
        stop_date = cleaned_data.get('stop_date')
        start_date = cleaned_data.get('start_date')
        if (stop_date and stop_date < start_date):
            msg = {'stop_date': f'Your stop date of {stop_date} is prior to '
                   f'start date of {start_date}.Please correct'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_took_arv(self, cleaned_data=None):
        took_arv = cleaned_data.get('maternal_arv_preg').took_arv
        if took_arv == YES:
            if not cleaned_data.get('arv_code'):
                msg = {'arv_code':
                       'You indicated that participant started ARV(s) during '
                       'this pregnancy. Please list them on maternal_arv table'}
                self._errors.update(msg)
                raise ValidationError(msg)
        else:
            if cleaned_data.get('arv_code'):
                msg = {'arv_code':
                       'You indicated that ARV(s) were NOT started during this '
                       'pregnancy. You cannot provide a list. Please Correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_historical_and_present_arv_start_dates(self, cleaned_data=None):
        maternal_visit = cleaned_data.get(
            'maternal_arv_preg').maternal_visit
        try:
            arv_history = self.arv_history_cls.objects.get(
                maternal_visit=maternal_visit)
            if arv_history.haart_start_date:
                if cleaned_data.get('start_date') < arv_history.haart_start_date:
                    msg = {'start_date':
                           'Your ARV start date in this pregnancy cannot be '
                           'before your Historical ARV date'}
                    self._errors.update(msg)
                    raise ValidationError(msg)
        except self.arv_history_cls.DoesNotExist:
            pass

    def validate_reason_for_stop(self):
        self.required_if_not_none(
            field='stop_date',
            field_required='reason_for_stop',
            required_msg='ARV stopped, please give reason for stop.',
        )
