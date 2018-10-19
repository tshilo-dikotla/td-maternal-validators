from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import NO

from ..constants import RESTARTED
from ..form_validators import MaternalArvHistoryFormValidator


class TestMaternalArvHistoryFormValidator(TestCase):

    def test_maternal_preg_on_haart_no_prior_restarted(self):
        cleaned_data = {'preg_on_haart': NO,
                        'prior_preg': RESTARTED}
        form_validator = MaternalArvHistoryFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('prior_preg', form_validator._errors)
