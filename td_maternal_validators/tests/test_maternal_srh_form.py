from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import YES
from .models import ListModel
from ..form_validators import MaternalSrhFormValidator


class TestMaternalSrhForm(TestCase):

    def test_is_contr_init_YES_contr_list_required(self):
        ListModel.objects.create(name='pills', short_name='Pills')
        ListModel.objects.create(name='iud', short_name='IUD')

        cleaned_data = {
            'is_contraceptive_initiated': YES,
            'contr': None
        }
        form_validator = MaternalSrhFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contr', form_validator._errors)

    def test_is_contr_init_YES_contr_list_provided(self):
        ListModel.objects.create(name='pills', short_name='Pills')
        ListModel.objects.create(name='iud', short_name='IUD')

        cleaned_data = {
            'is_contraceptive_initiated': YES,
            'contr': ListModel.objects.all()
        }
        form_validator = MaternalSrhFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
