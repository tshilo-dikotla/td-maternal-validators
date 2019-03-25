from edc_appointment.form_validators import (
    AppointmentFormValidator as BaseAppointmentFormValidator)


class AppointmentFormValidator(BaseAppointmentFormValidator):

    appointment_model = 'edc_appointment.appointment'

    def clean(self):
        super().clean()

    def validate_appt_new_or_complete(self):
        pass
