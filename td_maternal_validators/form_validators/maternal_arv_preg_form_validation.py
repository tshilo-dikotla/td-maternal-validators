from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django import forms
from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .form_validator_mixin import TDFormValidatorMixin
from edc_appointment.models import Appointment
from td_maternal.models import MaternalArvPreg, MaternalArv


def get_previous_visit(visit_obj, timepoints, subject_identifier):
    position = timepoints.index(
        visit_obj.appointment.visit_code)
    timepoints_slice = timepoints[:position]
    visit_model = django_apps.get_model(visit_obj._meta.label_lower)

    if len(timepoints_slice) > 1:
        timepoints_slice.reverse()
    for point in timepoints_slice:
        try:
            previous_appointment = Appointment.objects.filter(
                subject_identifier=subject_identifier, visit_code=point).order_by('-created').first()
            return visit_model.objects.filter(appointment=previous_appointment).order_by('-created').first()
        except Appointment.DoesNotExist:
            pass
        except visit_model.DoesNotExist:
            pass
        except AttributeError:
            pass
    return None


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
        self.validate_previous_maternal_arv_preg_arv_start_dates()

    def validate_previous_maternal_arv_preg_arv_start_dates(self):
        """Confirms that the ARV start date is equal to Maternal ARV
        start date unless stopped.
        """
        cleaned_data = self.cleaned_data
        subject_identifier = cleaned_data.get(
            'maternal_visit').appointment.subject_identifier
        previous_visit = get_previous_visit(
            visit_obj=cleaned_data.get('maternal_visit'),
            timepoints=['1000M', '1020M', '2000M'],
            subject_identifier=subject_identifier)

        if previous_visit:
            previous_arv_preg = MaternalArv.objects.filter(
                maternal_arv_preg__maternal_visit__appointment_subject__subject_identifier=subject_identifier,
                stop_date__isnull=True).order_by('-start_date').first()
            if previous_arv_preg:
                if previous_arv_preg.start_date:
                    start_date = cleaned_data.get('start_date')
                    if start_date != previous_arv_preg.start_date:
                        raise forms.ValidationError(
                            "ARV's were not stopped in this pregnancy, most recent ARV date was"
                            "{}, dates must match, got {}.".format(
                                previous_arv_preg.start_date, start_date))
