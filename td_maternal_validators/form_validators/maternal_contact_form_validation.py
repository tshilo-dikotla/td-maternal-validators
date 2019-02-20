from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator


class MaternalContactFormValidator(FormValidator):

    maternal_locator_model = 'td_maternal.maternallocator'

    @property
    def maternal_locator_cls(self):
        return django_apps.get_model(self.maternal_locator_model)

    def clean(self):
        cleaned_data = self.cleaned_data
        locator = self.maternal_locator
        if self.maternal_locator:
            if cleaned_data.get('contact_type') == 'voice_call' and locator.may_follow_up != YES:
                msg = {'may_follow_up':
                       f'Maternal Locator says may_follow_up: {locator.may_follow_up}, '
                       'you cannot call participant if they did not give permission.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            if cleaned_data.get('contact_type') == 'text_message' and locator.may_sms_follow_up != YES:
                msg = {'may_follow_up':
                       f'Maternal Locator says may_sms_follow_up: {locator.may_sms_follow_up}, '
                       'you cannot sms participant if they did not give permission.'}
                self._errors.update(msg)
                raise ValidationError(msg)
        else:
            msg = {'report_datetime':
                   f'Maternal Locator not found, please add Locator before proceeding.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        self.required_if(
            YES,
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
