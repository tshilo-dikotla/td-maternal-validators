from dateutil.relativedelta import relativedelta
from django.forms import forms
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import NO

from ..constants import NEVER_STARTED
from ..form_validators import MarternalArvPostFormValidator
from .models import MaternalVisit, MaternalConsent, MaternalArvPostAdh


class MaternalArvPostFormValidator(TestCase):

    def setUp(self):
        self.subject_consent = MaternalConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment)
        maternal_arv_post_adh = MarternalArvPostFormValidator.maternal_arv_post_adh
        maternal_arv_post_adh = maternal_arv_post_adh.replace(
            'td_maternal', 'td_maternal_validators')
        MarternalArvPostFormValidator.maternal_arv_post_adh = maternal_arv_post_adh

    @tag('c')
    def test_arv_status_no_invalid(self):
        cleaned_data = {'on_arv_since': NO,
                        'arv_status': NEVER_STARTED}
        MaternalArvPostAdh.objects.create(
            maternal_visit=self.maternal_visit)
        form_validator = MarternalArvPostFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)
