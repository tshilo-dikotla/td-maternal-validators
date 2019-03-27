from edc_appointment.form_validators import (
    AppointmentFormValidator as BaseAppointmentFormValidator)
from .crf_form_validator import TDCRFFormValidator


class AppointmentFormValidator(TDCRFFormValidator,
                               BaseAppointmentFormValidator):

    appointment_model = 'edc_appointment.appointment'

    def clean(self):
        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get('subject_identifier')
        super().clean()

    def validate_appt_new_or_complete(self):
        pass
