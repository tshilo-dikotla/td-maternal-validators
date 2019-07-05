from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_form_validator import TDCRFFormValidator
from .form_validator_mixin import TDFormValidatorMixin


class MaternalContactFormValidator(TDCRFFormValidator,
                                   TDFormValidatorMixin,
                                   FormValidator):

    maternal_locator_model = 'td_maternal.maternallocator'

    @property
    def maternal_locator_cls(self):
        return django_apps.get_model(self.maternal_locator_model)

    def clean(self):
        cleaned_data = self.cleaned_data
        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        if self.instance and not self.instance.id:
            self.validate_offstudy_model()

        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))

        locator = self.maternal_locator
        if self.maternal_locator:
            if (cleaned_data.get('contact_type') == 'voice_call'
                    and locator.may_call != YES):
                msg = {'contact_type':
                       f'Maternal Locator says may_call: {locator.may_call}, '
                       'you cannot call participant if they did not give '
                       'permission.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            if (cleaned_data.get('contact_type') == 'text_message'
                    and locator.may_sms != YES):
                msg = {'contact_type':
                       f'Maternal Locator says may_sms: {locator.may_sms}, '
                       'you cannot sms participant if they did not give '
                       'permission.'}
                self._errors.update(msg)
                raise ValidationError(msg)
        else:
            msg = {'__all__': 'Maternal Locator not found, please add '
                   'Locator before proceeding.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        self.validate_other_specify(
            field='call_reason',)

        self.required_if(
            YES,
            inverse=False,
            field='contact_success',
            field_required='contact_comment')

    @property
    def maternal_locator(self):
        cleaned_data = self.cleaned_data
        try:
            return self.maternal_locator_cls.objects.get(
                subject_identifier=cleaned_data.get('subject_identifier'))
        except self.maternal_locator_cls.DoesNotExist:
            return None
