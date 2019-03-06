from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django import forms
from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .form_validator_mixin import TDFormValidatorMixin
from edc_appointment.models import Appointment


class MaternalArvPregFormValidator(TDFormValidatorMixin, FormValidator):

    def clean(self):

        self.applicable_if(
            YES,
            field='is_interrupt',
            field_applicable='interrupt',
        )

        self.validate_other_specify(
            field='interrupt',
            other_specify_field='interrupt_other',
            required_msg='Please give reason for interruption'
        )
