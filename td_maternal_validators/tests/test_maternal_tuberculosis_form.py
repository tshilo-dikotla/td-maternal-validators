from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import YES, NO
from ..form_validators import MaternalTuberculosisHistoryFormValidator


class TestMaternalSubstanceDuringPregForm(TestCase):

    def setUp(self):
        self.cleaned_data = {
            'coughing': YES,
        }
        pass

    def test_coughing_relation_required(self):
        pass

    def test_coughing_relation_not_required(self):
        pass

    def test_diagnosis_relation_required(self):
        pass

    def test_diagnosis_relation_not_required(self):
        pass

    def test_tuberculosis_treatment_relation_required(self):
        pass

    def test_tuberculosis_treatment_relation_not_required(self):
        pass
